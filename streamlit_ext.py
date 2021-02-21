import streamlit
import hashlib
from streamlit.hashing import update_hash, HashReason


class _Proxy(dict):
    def __init__(self):
        dict.__init__(self)

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, item):
        if item not in self:
            val = _Proxy()
            dict.__setitem__(self, item, val)
            return val

        return dict.__getitem__(self, item)


class SessionObject(dict):
    def __init__(self, uuid: str):
        dict.__init__(self, session_id=uuid, components={}, values=_Proxy())

    @property
    def session_id(self) -> str:
        return dict.__getitem__(self, 'session_id')

    @property
    def _components(self) -> dict:
        return dict.__getitem__(self, 'components')

    @property
    def values(self) -> _Proxy:
        return dict.__getitem__(self, 'values')

    def __getitem__(self, item):
        return self._components[item]

    def __setitem__(self, key, value):
        raise KeyError(key)


def get_session_object():
    if not streamlit.get_option("client.caching"):
        raise RuntimeError("Can not use session object if client cache is disabled")

    @streamlit.cache(allow_output_mutation=True)
    def get_session_obj_impl(uuid: str):
        return SessionObject(uuid)

    ctx = streamlit.report_thread.get_report_ctx()
    if not ctx:
        raise RuntimeError("Please add this thread to reach report context")

    return get_session_obj_impl(ctx.session_id)


class _ValueChange(dict):
    def __init__(self, unique_id: str):
        dict.__init__(self, _unique_id=unique_id, _old_value=None, _value=None, _frozen_value=None, _frozen=None)
        self.old_args = None

    @property
    def unique_id(self) -> str:
        return dict.__getitem__(self, '_unique_id')

    @property
    def value(self):
        return dict.__getitem__(self, '_value')

    @property
    def old_value(self):
        return dict.__getitem__(self, '_old_value')

    @property
    def frozen_value(self):
        return dict.__getitem__(self, '_frozen_value')

    @property
    def changed(self) -> bool:
        return self.old_value is not None and self.value != self.old_value

    @property
    def first_run(self) -> bool:
        return self.old_value is None and self.frozen_value is None

    def set_freeze(self, val: bool = True):
        dict.__setitem__(self, '_frozen', val)
        if not val:
            if self.frozen_value is not None:
                self.set_value(self.frozen_value)
            dict.__setitem__(self, '_frozen_value', None)

    def is_frozen(self) -> bool:
        return dict.__getitem__(self, '_frozen')

    def set_value(self, val):
        if self.is_frozen():
            dict.__setitem__(self, '_frozen_value', val)
        else:
            dict.__setitem__(self, '_old_value', self.value)
            dict.__setitem__(self, '_value', val)

    @property
    def run_value(self):
        return self.frozen_value if self.is_frozen() else self.value

    def __bool__(self):
        return bool(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __str__(self):
        return str(self.value)

    def __iter__(self):
        return iter(self.value)

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __len__(self):
        return len(self.value)

    def __lt__(self, other):
        return self.value < other

    def __gt__(self, other):
        return not self < other and self != other

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return self < other or self == other

    def __abs__(self):
        return abs(self.value)

    def __getitem__(self, item):
        return self.value[item]

    def __setitem__(self, key, value):
        raise KeyError(key)

    def __getattr__(self, item):
        return getattr(self.value, item)

    def __repr__(self):
        return f'{self.unique_id}: {self.value}' + (
            f' (old: {self.old_value})' if self.old_value is not None else '') + (f' (frozen' + (
            f', val: {self.frozen_value}' if self.frozen_value is not None else '') + ')' if self.is_frozen() else '')

    def __add__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other


def _wrapper_wrapped(in_fun):
    session_obj = get_session_object()
    def wrapped_fun(*args, **kwargs):

        value_hasher = hashlib.new("md5")
        value_hasher.update(in_fun.__name__.encode())

        value_path = kwargs.get("as_value")
        if value_path:
            del kwargs["as_value"]

        if args:
            update_hash(
                args,
                hasher=value_hasher,
                hash_funcs={streamlit.delta_generator.DeltaGenerator: repr,
                            _ValueChange: repr},
                hash_reason=HashReason.CACHING_FUNC_OUTPUT,
                hash_source=in_fun,
            )

        if kwargs:
            update_hash(
                kwargs,
                hasher=value_hasher,
                hash_funcs={streamlit.delta_generator.DeltaGenerator: repr,
                            _ValueChange: repr},
                hash_reason=HashReason.CACHING_FUNC_OUTPUT,
                hash_source=in_fun,
            )

        key = repr(id(in_fun.__self__)) + ' ' + in_fun.__name__ + ' ' + value_hasher.hexdigest()

        value_change = session_obj._components.get(key, None)
        if value_change is None:
            value_change = _ValueChange(key)
            session_obj._components[key] = value_change

        value = in_fun(*args, **kwargs)
        value_change.set_value(value)

        if value_path and not value_change.is_frozen():
            session_values = session_obj.values
            paths = value_path.split('.')
            for path in paths[:-1]:
                session_values = session_values[path]
            session_values[paths[-1]] = value
        return value_change

    return wrapped_fun


for k, fun in streamlit.__dict__.items():
    if k in ['button', 'checkbox', 'radio', 'selectbox', 'multiselect', 'slider', 'select_slider', 'text_input',
             'number_input', 'text_area', 'date_input', 'time_input', 'file_uploader', 'color_picker']:
        globals()[k] = _wrapper_wrapped(fun)

    elif callable(fun) and not k.startswith('_'):
        globals()[k] = fun


sidebar = streamlit.sidebar
