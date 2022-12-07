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
        m = np.logical_or(df[col].str.contains(keyword), m)
    return m

def get_mask_for_keyword_list(df, keyword_list, search_cols=["autor", "titulo"]):
    """
    Get a mask from a dataframe based on a list of texts
    """
    m = False
    for keyword in keyword_list:
        m = np.logical_or(get_mask_for_keyword(df, keyword, search_cols), m)
    return m

def create_card(row, c):
    """
    Creates a card with the information of a row, using streamlit elements
    row has (at least) columns: ["Evento", "Lugar", "Fecha", "Tipo", "Autor", "Titulo", "Video", "Otros hipervínculos"]
    """
    c.caption(f"{row['Evento'].strip()}-{row['Lugar'].strip()}-{row['Fecha'].strip()} ")
    c.markdown(f"**{row['Autor'].strip()}**")
    c.markdown(f"{row['Tipo'].strip()}: {row['Titulo'].strip()}")
    c.markdown(f"{row['Video'].strip()}", unsafe_allow_html=True)
    

