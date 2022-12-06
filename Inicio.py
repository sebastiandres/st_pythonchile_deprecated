import streamlit as st
import pandas as pd
import numpy as np
from unidecode import unidecode

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


st.set_page_config(page_title="Contenido audiovisual Python Chile", page_icon=":chile:", layout="wide", initial_sidebar_state="expanded")
st.title('Python Chile: Contenidos Audiovisuales')

public_googlesheet = "https://docs.google.com/spreadsheets/d/1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws/edit?usp=sharing"
sheet_id = "1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df = pd.read_csv(url, dtype=str).fillna("")

# Lower all the text
df_lower = df.copy()
df_lower.columns = df_lower.columns.str.lower()
for col in df_lower.columns:
    df_lower[col] = df_lower[col].apply(lambda x: unidecode(x.lower()))
df['Video'] = df['Video'].apply(make_clickable)

show_cols = ["Evento", "Lugar", "Fecha", "Tipo", "Autor", "Titulo", "Video", "Otros hipervínculos"]

with st.form("Búsqueda"):
    c1, c2 = st.columns([10,1])
    c2.markdown(""); c2.markdown(""); 
    text = c1.text_input("Buscar por autor, título, descripción o tags. Separa conceptos por punto y coma (;)")
    text = unidecode(text.lower())
    keyword_list = [keyword.strip() for keyword in text.split(";")]
    # Every form must have a submit button.
    if c2.form_submit_button("Submit"):
        mask = get_mask_for_keyword_list(df_lower, keyword_list)
        df_search = df.loc[mask, show_cols].to_html(escape=False, index=False)
        # convert to html before showing so urls open easily
        st.write(df_search, unsafe_allow_html=True)