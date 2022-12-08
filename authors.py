import streamlit as st

from helpers import *

def get_authors_data():
    # Shared gsheet_id
    gsheet_id = "1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws"
    # Data for the authors (autores)
    df_authors = read_googlesheet(gsheet_id, "personas", ["Autor"])
    # Add a column with the clean name
    df_authors["author_clean_name"] = df_authors["Autor"].apply(clean_name)
    # Normalize the column names
    df_authors.columns = [ unidecode(s.lower().strip()) for s in df_authors.columns]
    return df_authors


def is_author_in_authors(df_authors, author):
    """
    """
    author_clean_name = clean_name(author) 
    return author_clean_name in df_authors["author_clean_name"].values


def display_author(df_authors, df_events, author_search_name):
    """
    """
    # Start the page
    st.caption('Python Chile: Autores')
    author_clean_name = clean_name(author_search_name)
    # Try to find some talks by the author
    df_author_events = df_events.loc[df_events["author_clean_name"] == author_clean_name, :].reset_index()
    if len(df_author_events) == 0:
        display_404_author(author_search_name)
        return
    # Get social media for the author
    df_author_links = df_authors.loc[df_authors["author_clean_name"] == author_clean_name, :].reset_index()
    if len(df_author_links) > 0:
        companies_list = ["twitter", "linkedin", "github"]
        known_companies_html = []
        for company in companies_list:
            if company in df_author_links.columns:
                link = df_author_links[company].values[0]
                if len(link)>0:
                    image_link = f"https://github.com/sebastiandres/st_pythonchile/blob/main/images/social_media_icons/{company}.png?raw=true"
                    html = clickable_image_html(link, image_link, style="width:25px;")
                    known_companies_html.append(html)
        html_social_media = "".join(known_companies_html)
    else:
        html_social_media = " "
    # If there is a match, then show the author page
    author_display_name = df_author_events["Autor"].values[0]
    st.title(author_display_name)
    st.components.v1.html(html_social_media, height=50)
    # Show the cards
    N_cards_per_col = 5
    for n_row, row in df_author_events.iterrows():
        i = n_row%N_cards_per_col
        if i==0:
            st.write("")
            cols = st.columns(N_cards_per_col, gap="large")
        create_card(row, cols[n_row%N_cards_per_col])
    add_color_to_cards()
    # Show table!
    #st.write(df_author_links)
    #st.write(df_author_events)

def display_404_author(author):
    """
    """
    st.title("404")
    st.write(f"No se encontró el autor {author} entre los autores registrados.")
    if st.button("Volver a la página principal"):
        st.experimental_set_query_params()