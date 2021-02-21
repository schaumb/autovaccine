import streamlit
import sys
import importlib


streamlit.set_page_config(page_title="Hack&Heal")
streamlit.markdown('''<style>
.circle {
  -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome and Opera */
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  display: inline-block;
  font-style: normal;
  font-variant: normal;
  text-rendering: auto;
  border-radius: 50%;
  shape-outside: circle(50%);
  width: 170px; height: 170px;
  font-size: 70px;  
  text-align: center;
  color: black;
  vertical-align: middle;
  line-height: 70px;
}
.circle:hover {
  background-color: lime;
  cursor: pointer;
}
</style>''',  unsafe_allow_html=True)




streamlit.header("💉 COVID-19 vakcina app")

if "login" not in sys.modules:
    import login
else:
    importlib.reload(importlib.import_module("login"))

streamlit.sidebar.subheader("Menüpontok")
with streamlit.sidebar.beta_container():
    if streamlit.button("💉 Választó menü"):
        streamlit.experimental_set_query_params()
    streamlit.subheader('Pácienseknek')
    if streamlit.button("🧾️ Előzetes nyilatkozat"):
        streamlit.experimental_set_query_params(sub="perm_notice", pre=True)
    if streamlit.button("🛡️ Hozzájáruló nyilatkozat"):
        streamlit.experimental_set_query_params(sub="perm_notice")
    if streamlit.button("📆 Időpont változtatás"):
        streamlit.experimental_set_query_params(sub="idopont")
    streamlit.subheader('Háziorvosoknak')
    if streamlit.button("📝 Páciensek elbírálása"):
        streamlit.experimental_set_query_params(sub="elbiralas")
    if streamlit.button("🗓️ Időpont foglalás"):
        streamlit.experimental_set_query_params(sub="foglalas")
    if streamlit.button("📣 Kiértesítés"):
        streamlit.experimental_set_query_params(sub="kiertesites")
    streamlit.subheader('Oltóközpontoknak')
    if streamlit.button("🧑‍⚕️ Napi páciensek"):
        streamlit.experimental_set_query_params(sub="mai_nap")
    if streamlit.button("📖 Új adatok bevitele"):
        streamlit.experimental_set_query_params(sub="uj_adatok")
    if streamlit.button("💼 Report készítése"):
        streamlit.experimental_set_query_params(sub="reports")
    streamlit.markdown('---')

subpage = streamlit.experimental_get_query_params().get("sub")
if subpage and isinstance(subpage, list):
    subpage = subpage[-1]

if subpage and subpage not in sys.modules:
    try:
        importlib.import_module(subpage)
        streamlit.stop()
    except streamlit.StopException:
        raise
    except:
        pass
elif subpage:
    importlib.reload(importlib.import_module(subpage))
    streamlit.stop()


with streamlit.beta_expander("Pácienseknek", expanded=True):
    with streamlit.beta_container():
        b1, b2, b3 = streamlit.beta_columns(3)
        with b1:
            streamlit.markdown('<div click_it="🧾️ Előzetes nyilatkozat" class="circle"><p></p>🧾<p style="font-size: 30px; line-height:1.4">Előzetes nyilatkozat</p></div>', unsafe_allow_html=True)
        with b2:
            streamlit.markdown('<div click_it="🛡️ Hozzájáruló nyilatkozat" class="circle"><p></p>🛡<p style="font-size: 30px; line-height:1.4">Hozzájáruló nyilatkozat</p></div>', unsafe_allow_html=True)
        with b3:
            streamlit.markdown('<div click_it="📆 Időpont változtatás" class="circle"><p></p>📆<p style="font-size: 30px; line-height:1.4">Időpont változtatás</p></div>', unsafe_allow_html=True)

with streamlit.beta_expander("Háziorvosoknak", expanded=True):
    with streamlit.beta_container():
        b1, b2, b3 = streamlit.beta_columns(3)
        with b1:
            streamlit.markdown('<div click_it="📝 Páciensek elbírálása" class="circle"><p></p>📝<p style="font-size: 30px; line-height:1.4">Páciensek elbírálása</p></div>', unsafe_allow_html=True)
        with b2:
            streamlit.markdown('<div click_it="🗓️ Időpont foglalás" class="circle"><p></p>🗓️<p style="font-size: 30px; line-height:1.4">Időpont foglalás</p></div>', unsafe_allow_html=True)
        with b3:
            streamlit.markdown('<div click_it="📣️ Kiértesítés" class="circle"><p></p>📣️<p style="font-size: 30px; line-height:1.4">Kiértesítés</p></div>', unsafe_allow_html=True)

with streamlit.beta_expander("Oltóközpontoknak", expanded=True):
    with streamlit.beta_container():
        b1, b2, b3 = streamlit.beta_columns(3)
        with b1:
            streamlit.markdown('<div click_it="🧑‍⚕️ Napi páciensek" class="circle"><p></p>🧑‍⚕️<p style="font-size: 30px; line-height:1.4">Napi páciensek</p></div>', unsafe_allow_html=True)
        with b2:
            streamlit.markdown('<div click_it="📖 Új adatok bevitele" class="circle"><p></p>📖<p style="font-size: 30px; line-height:1.4">Új adatok bevitele</p></div>', unsafe_allow_html=True)
        with b3:
            streamlit.markdown('<div click_it="💼 Report készítése" class="circle"><p></p>💼<p style="font-size: 30px; line-height:1.4">Report készítése</p></div>', unsafe_allow_html=True)


streamlit.markdown('''
<iframe width='0' height='0' srcdoc="<script>
    [...parent.document.getElementsByClassName('circle')].forEach(c => c.onclick = 
        e => [...parent.document.getElementsByTagName('button')].filter(f => f.innerText == c.getAttribute('click_it'))[0].click()); 
</script>" />
''', unsafe_allow_html=True)
