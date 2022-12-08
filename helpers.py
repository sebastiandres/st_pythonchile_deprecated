import streamlit as st
import pandas as pd
import numpy as np
from unidecode import unidecode
import random
from collections import defaultdict

image_dict = defaultdict(lambda: "https://github.com/sebastiandres/st_pythonchile/blob/main/images/python_chile.png?raw=true")
image_dict["Pycon 2022"] = "https://github.com/sebastiandres/st_pythonchile/blob/main/images/pycon_2022.png?raw=true"
image_dict["Pyday 2020"] = "https://github.com/sebastiandres/st_pythonchile/blob/main/images/pyday_2020.png?raw=true"
image_dict["Sin registro"] = "https://github.com/sebastiandres/st_pythonchile/blob/main/images/sin_registro.png?raw=true"

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    youtube = "yutú:"
    text = link.replace("https://www.youtube.com/watch?v=", youtube).replace("https://youtu.be/", youtube)
    return f'<a target="_blank" href="{link}" style="background-size: cover;">{text}</a>'


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
    link = row["Video"].strip()
    evento = row["Evento"].strip()
    image_link = image_dict[evento]
    clickable_image = f'<a href="{link}" target="_blank"> <img src="{image_link}" style="width:100%;"> </a>'
    with c:
        #st.write(clickable_image)
        st.caption(f"{row['Evento'].strip()} - {row['Lugar'].strip()} - {row['Fecha'].strip()} ")
        st.markdown(f"**{row['Autor'].strip()}**")
        st.components.v1.html(clickable_image)
        st.markdown(f"{row['Tipo'].strip()}: {row['Titulo'].strip()}")
        

def add_color_to_cards():
    """
    Adds color to the expanders.
    Users don't need to call this function, is executed by default.
    """
    # Define your javascript
    my_js = """
    var cards = window.parent.document.getElementsByClassName("css-vhjbnf");
    for (var i = 0; i < cards.length; i++) {
        let card = cards[i];
        // See if there´s content in the card
        N_chars_in_cards = String(card.firstChild.innerHTML).length;
        if (N_chars_in_cards >100){
            card.style.border = "solid";
            card.style.borderColor = "#E4F6F8";
            card.style.borderWidth = "2px";
            card.style.padding = "10px";
            card.style.borderRadius = "10px";
        }
    }    
    """

    # Wrapt the javascript as html code
    my_html = f"<script>{my_js}</script>"

    # Execute your app
    st.components.v1.html(my_html, height=0, width=0)

    return