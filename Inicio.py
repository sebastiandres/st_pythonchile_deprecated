import streamlit as st

from helpers import *

st.set_page_config(page_title="Contenido audiovisual Python Chile", page_icon="https://pythonchile.cl/images/favicon.png", 
                layout="wide", initial_sidebar_state="expanded")
st.title('Python Chile: Contenidos Audiovisuales')

# The data on the google sheet
#['Evento', 'Lugar', 'Fecha', 'Orden', 'Track', 'Tipo', 'Programa Evento',
#       'Autor', 'Titulo', 'Video', 'Palabras clave', 'Descripción',
#       'Otros hipervínculos']
public_googlesheet = "https://docs.google.com/spreadsheets/d/1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws/edit?usp=sharing"
sheet_id = "1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")
df.sort_values(["Fecha", "Orden", "Track"], ascending=False, inplace=True)

# Filter incomplete rows
df = df.loc[df["Autor"] != "", :]
df = df.loc[df["Titulo"] != "", :]

# A little bit of cleaning, to make searching more easy
# df_lower should get the columns
# ['evento', 'lugar', 'fecha', 'orden', 'track', 'tipo', 'programa evento', 'autor', 'titulo', 'video', 'palabras clave', 'descripción', 'otros hipervínculos']
# Lower all the text
df_lower = df.copy()
df_lower.columns = df_lower.columns.str.lower()
for col in df_lower.columns:
    df_lower[col] = df_lower[col].apply(lambda x: unidecode(x.lower()))

# We use the following columns to show data
show_cols = ["Evento", "Lugar", "Fecha", "Tipo", "Autor", "Titulo", "Video", "Otros hipervínculos"]

# Intro text
st.caption(f"Descubre y aprende entre los más de {df.shape[0]} charlas, keynotes y talleres que hemos realizado en Python Chile.")
c1, c2, c3 = st.columns([8,1,1])
# The search bar
ejemplos = ["data science", "machine learning", "streamlit", "pyladies", "comunidad", "industria"]
if "ejemplo" not in st.session_state:
    st.session_state.ejemplo = ejemplos[random.randint(0, len(ejemplos)-1)]
text_search = c1.text_input("Buscar por autor, título, descripción o tags. Separa conceptos por punto y coma (;)",
                            placeholder=st.session_state.ejemplo)
text_search = unidecode(text_search.lower())
# Get keywords from search bar
keyword_list = [keyword.strip() for keyword in text_search.split(";")]
# Add options
talk_options = ["Cualquiera", "Charla", "Keynote", "Taller"]
type_sel = c2.selectbox("Tipo", talk_options)
c3.markdown(""); c3.markdown(""); 
rec_required = c3.checkbox("Grabado", value=False)

# Configure how many cards
N_cards_per_col = 5

if text_search:
    mask = get_mask_for_keyword_list(df_lower, keyword_list)
    if type_sel != talk_options[0]:
        mask_new = df_lower["tipo"] == type_sel.lower()
        mask = np.logical_and(mask, mask_new)
    if rec_required:
        mask_new = df_lower["video"] != ""
        mask = np.logical_and(mask, mask_new)
    df_search = df.loc[mask, show_cols].reset_index()
    # Show the cards
    N_cards_per_col = 5
    for n_row, row in df_search.iterrows():
        i = n_row%N_cards_per_col
        if i==0:
            st.write("")
            cols = st.columns(N_cards_per_col, gap="large")
        create_card(row, cols[n_row%N_cards_per_col])
else:
    # Configure how many cards
    N_cards =  N_cards_per_col * 1
    # Show the cards
    st.write("#### Últimos videos disponibles")
    df_latest = df[show_cols].head(N_cards).reset_index()
    for n_row, row in df_latest.iterrows():
        i = n_row%N_cards_per_col
        if i==0:
            st.write("")
            cols = st.columns(N_cards_per_col, gap="large")
        create_card(row, cols[n_row%N_cards_per_col])
    st.write("")
    st.write("#### Videos seleccionados aleatoriamente")
    df_random = df[show_cols].sample(N_cards).reset_index()
    for n_row, row in df_random.iterrows():
        i = n_row%N_cards_per_col
        if i==0:
            st.write("")
            cols = st.columns(N_cards_per_col, gap="large")
        create_card(row, cols[i])

# Add color to cards
add_color_to_cards()