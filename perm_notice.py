import streamlit
import streamlit_drawable_canvas
import datetime

streamlit.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
streamlit.subheader("Hozzájáruló nyilatkozat a COVID-19 fertőzés elleni vakcina beadásához")
streamlit.subheader("Kérjük válaszoljon az alábbi kérdésekre! (Jelöljön be minden megfelelőt)")

questions = [
    "Van-e tartós, krónikus betegsége? (cukorbetegség, magas vérnyomás, asztma, szív-, vesebetegség stb.)",
    "Rendszeresen szed-e gyógyszert?",
    "Van-e bármilyen allergiája (élelmiszer, gyógyszer, egyéb)?",
    "Vérvétel vagy oltás során volt-e előzőleg rosszulléte?",
    "Védőoltás beadásátkövetően volt-e anafilaxiás reakciója?<br />"
    "<b>(Megjegyzés:ismeretlen gyógyszer okozta anafilaxia kizáró ok, antibiotikumallergia, lázcsillapító allergia NEM!)</b>",
    "Az elmúlt 3 hónapban kapott-e az immunrendszerét gyengítő kezelést, "
    "mint például: kortizon, prednizon, egyéb szteroidok, immunbiológiai készítmények "
    "vagy daganatellenes szerek, ill. sugárkezelést?",
    "Volt-e valaha görcsrohama, idegrendszeri problémája, bénulása?",
    "Szenved-e vérképzőszervi betegségben, fokozott vérzékenységben?",
    "Jelenleg várandós-e?",
    "Tervez-e várandósságot 2 hónapon belül?",
    "Szoptat-e?"
]

questions_short_term = [
    "Volt-e valamilyen akut betegségeaz elmúlt 4 hétben?",
    "Volt-e lázas beteg az elmúlt 2 hétben?<br />"
    "<b>(Megjegyzés: akut lázas betegség kizáró ok, 3 hónapon belül PCR igazolt fertőzés kizáró ok)</b>",
    "Szenved-e olyan autoimmun betegségben, melynek épp aktív fázisa zajlik?",
    "Kapott-e védőoltást az elmúlt 2hétben?",
    "Jelenleg van-e bármilyen panasza?"
]

ask_questions = questions.copy()

if not streamlit.experimental_get_query_params().get("pre"):
    ask_questions.extend(questions_short_term)

for count, question in enumerate(ask_questions):
    q, v = streamlit.beta_columns([3, 1])
    q.markdown("<p></p>" + question, unsafe_allow_html=True)
    with v:
        streamlit.radio("", ["igen", "nem"], index=1, key=question)
    streamlit.markdown("---")

streamlit.markdown(f'Dátum: {datetime.date.today().strftime("%Y. %m. %d.")}')

streamlit.markdown("Aláírás")
streamlit_drawable_canvas.st_canvas(fill_color="black", stroke_width=1, height=100)

if streamlit.button("Mentés PDF-be"):
    streamlit.markdown('''
    <iframe width='0' height='0' srcdoc='
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <script src="https://unpkg.com/jspdf@latest/dist/jspdf.umd.min.js"></script>
    <script>
    parent.html2canvas = html2canvas;
    signiture = parent.document.getElementsByTagName("iframe")[0];
    signitureB = signiture.contentWindow.document.body.getElementsByClassName("lower-canvas")[2];
    main_stuff = parent.document.getElementsByClassName("main")[0].childNodes[0];
    parent.html2canvas(main_stuff).then(canvas => {
        parent.html2canvas(signitureB).then(canvas2 => {
            var newCanvas = document.createElement("canvas");
            var context = newCanvas.getContext("2d");
            newCanvas.width = canvas.width;
            newCanvas.height = canvas.height;
            x_pos = signiture.getBoundingClientRect().top - main_stuff.getBoundingClientRect().top;
            y_pos = signiture.getBoundingClientRect().left - main_stuff.getBoundingClientRect().left;
            context.drawImage(canvas, 0, 0);
            context.drawImage(canvas2, y_pos,    x_pos);
            let width = newCanvas.width; 
            let height = newCanvas.height;
            if(newCanvas.width > newCanvas.height)
              pdf = new jspdf.jsPDF("l", "px", [newCanvas.width, newCanvas.height]);
            else
              pdf = new jspdf.jsPDF("p", "px", [newCanvas.height, newCanvas.width]);
            pdf.addImage(newCanvas, "PNG", 0, 0, pdf.internal.pageSize.getWidth(), pdf.internal.pageSize.getHeight());
            pdf.save("download.pdf");
        })
    });
    </script>'></iframe>
    ''', unsafe_allow_html=True)
