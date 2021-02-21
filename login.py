import streamlit_ext as streamlit

values = streamlit.get_session_object().values
with streamlit.sidebar:
    em = streamlit.empty()
    with em:
        taj = streamlit.text_input("Adja meg a taj számát / a páciens taj számát", as_value='taj')
    if not values.logined:
        if taj:
            taj = taj.replace('-', '')
            try:
                int(taj)
                if len(taj) != 9:
                    streamlit.error("Nem tűnik valós TAJ számnak. 9 számjegyből kell állnia.")
                    taj = ''
            except:
                streamlit.error("A TAJ szám csak számokat, és elválasztó kötőjeleket tartalmazhat")
                taj = ''

        if taj:
            values.logined = True

    if values.logined:
        with em:
            em.write("")
        streamlit.markdown("Személy: " + "Kiss Béla")
        streamlit.markdown("Születési idő: 1920.06.30.")

        if streamlit.button("Más vagyok"):
            values.logined = False
            streamlit.experimental_rerun()
