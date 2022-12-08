import streamlit as st
import pandas as pd
import numpy as np
from unidecode import unidecode
import random
from collections import defaultdict
#from IPython import embed

image_dict = defaultdict(lambda: "https://github.com/sebastiandres/st_pythonchile/blob/main/images/python_chile.png?raw=true")
image_dict["Pycon 2022"] = "https://github.com/sebastiandres/st_pythonchile/blob/main/images/pycon_2022.png?raw=true"
image_dict["Pyday 2020"] = "https://github.com/sebastiandres/st_pythonchile/blob/main/images/pyday_2020.png?raw=true"
image_dict["Sin registro"] = "https://github.com/sebastiandres/st_pythonchile/blob/main/images/sin_registro.png?raw=true"

def clean_name(name):
    """
    """
    return unidecode(name.strip().replace(" ", "").replace(r"%20","").lower())


def read_googlesheet(sheet_id, sheet_name, sort_columns):
    """
    Reads a google sheet and returns a dataframe, sorted by the columns in sort_columns.
    if the public_googlesheet is "https://docs.google.com/spreadsheets/d/1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws/edit?usp=sharing"
    then the sheet_id is "1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws"
    The sheet_name is the name of the sheet in the google sheet
    """
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url, dtype=str).fillna("")
    df = df.sort_values(sort_columns, ascending=False, ignore_index=True)
    return df

def html_link(text, link, blank=True):
    # target _blank to open new window
    # extract clickable text to display for your link
    #youtube = "yutú:"
    #text = link.replace("https://www.youtube.com/watch?v=", youtube).replace("https://youtu.be/", youtube)
    if blank:
        return f'<a target="_blank" href="{link}">{text}</a>'
    else:
        return f'<a target="_top" href="{link}">{text}</a>'


def get_mask_for_keyword(df, keyword, search_cols=["autor", "titulo"]):
    """
    Get a mask from a dataframe based on a text
    """
    m = False
    for col in search_cols:
        m = np.logical_or(df[col].str.contains(keyword), m)
    return m


def clickable_image_html(link, image_link, style="width:100%;"):
    html = f'<a href="{link}" target="_blank"><img src="{image_link}" style="{style}"></a>'
    return html


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
    if link != "Sin registro":
        image_link = image_dict[evento]
        clickable_image = f'<a href="{link}" target="_blank"> <img src="{image_link}" style="width:100%;"> </a>'
    else:
        image_link = image_dict["Sin registro"]
        clickable_image = f'<img src="{image_link}" style="width:100%;">'
    with c:
        #st.write(clickable_image)
        st.caption(f"{row['Evento'].strip()} - {row['Lugar'].strip()} - {row['Fecha'].strip()} ")
        #st.markdown(f"**{row['Autor'].strip()}**")
        authors_html_list = []
        for author in row["Autor"].split(";"):
            authors_html_list.append(html_link(author, f"/?author={author}", blank=True))
        authors_html = " | ".join(authors_html_list)
        st.markdown(authors_html + clickable_image, unsafe_allow_html=True)
        #st.components.v1.html(authors_html + clickable_image)
        st.markdown(f"{row['Tipo'].strip()}: {row['Titulo'].strip()}")
        

def add_style():
    """
    Adds style so link are not blue
    """
    # Define style
    style = """
    a:link {
    color: inherit;
    text-decoration: none;
    }

    a:visited {
    color: inherit;
    text-decoration: none;
    }

    a:hover {
    color: red;
    text-decoration: underline;
    }

    a:active {
    color: red;
    text-decoration: underline;
    }
    """
    my_html = f"""
                <style>
                {style} 
                </style>
                """

    # Execute your app
    st.components.v1.html(my_html, height=0, width=0)

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
        // See if there's content in the card
        N_chars_in_cards = String(card.firstChild.innerHTML).length;
        if (N_chars_in_cards >100){
            card.style.border = "solid";
            card.style.borderColor = "#E4F6F8";
            card.style.borderWidth = "2px";
            card.style.padding = "10px";
            card.style.borderRadius = "10px";
            card.style.borderRadius = "10px";
            card.addEventListener("mouseover", function(event){card.style.borderColor = "red"})
            card.addEventListener("mouseout",  function(event){card.style.borderColor = "#E4F6F8"})
        }
    }    
    """

    # Wrapt the javascript as html code
    my_html = f"""
                <script>
                {my_js}
                </script>
                """
    # Execute your app
    st.components.v1.html(my_html, height=0, width=0)

    return