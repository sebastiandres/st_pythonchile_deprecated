import streamlit as st
import pandas as pd
import numpy as np
from unidecode import unidecode
import random

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    youtube = "yutú:"
    text = link.replace("https://www.youtube.com/watch?v=", youtube).replace("https://youtu.be/", youtube)
    return f'<a target="_blank" href="{link}">{text}</a>'


def get_mask_for_keyword(df, keyword, search_cols=["autor", "titulo"]):
    """
    Get a mask from a dataframe based on a text
    """
    m = False
    for col in search_cols:
        m = np.logical_or(df_lower[col].str.contains(keyword), m)
    return m

def get_mask_for_keyword_list(df, keyword_list, search_cols=["autor", "titulo"]):
    """
    Get a mask from a dataframe based on a list of texts
    """
    m = False
    for keyword in keyword_list:
        m = np.logical_or(get_mask_for_keyword(df, keyword, search_cols), m)
    return m


st.set_page_config(page_title="Contenido audiovisual Python Chile", page_icon="https://pythonchile.cl/images/favicon.png", 
                layout="wide", initial_sidebar_state="expanded")
st.title('Python Chile: Contenidos Audiovisuales')

public_googlesheet = "https://docs.google.com/spreadsheets/d/1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws/edit?usp=sharing"
sheet_id = "1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")
df.sort_values(["Fecha", "Orden", "Track"], ascending=False, inplace=True)

# Lower all the text
df_lower = df.copy()
df_lower.columns = df_lower.columns.str.lower()
for col in df_lower.columns:
    df_lower[col] = df_lower[col].apply(lambda x: unidecode(x.lower()))
df['Video'] = df['Video'].apply(make_clickable)

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

if text_search:
    mask = get_mask_for_keyword_list(df_lower, keyword_list)
    if type_sel != talk_options[0]:
        mask_new = df_lower["tipo"] == type_sel.lower()
        mask = np.logical_and(mask, mask_new)
    if rec_required:
        mask_new = df_lower["video"] != ""
        mask = np.logical_and(mask, mask_new)
    df_search = df.loc[mask, show_cols].to_html(escape=False, index=False)
    # convert to html before showing so urls open easily
    st.write(df_search, unsafe_allow_html=True)
else:
    st.write("#### Últimos videos disponibles")
    st.write(df[show_cols].head(3).to_html(escape=False, index=False), unsafe_allow_html=True)
    st.write("")
    st.write("#### Videos seleccionados aleatoriamente")
    st.write(df[show_cols].sample(3).to_html(escape=False, index=False), unsafe_allow_html=True)
