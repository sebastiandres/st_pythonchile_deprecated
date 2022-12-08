import streamlit as st

from helpers import *

def get_authors_data():
    # Shared gsheet_id
    gsheet_id = "1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws"
    # Data for the authors (autores)
    df_authors = read_googlesheet(gsheet_id, "personas", ["Autor"])
    # Add a column with the clean name
    df_authors["author_clean_name"] = df_authors["Autor"].apply(clean_name)
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
    st.title('Python Chile: Autores')
    author_clean_name = clean_name(author_search_name)
    df = df_authors.loc[df_authors["author_clean_name"] == author_clean_name, :]
    if len(df) == 0:
        display_404_author(author_search_name)
        return
    if len(df) > 1:
        st.write("Hay más de 1 autor con el mismo nombre.")
        st.write(df)
        return
    # If there is a match, then show the author page
    author_display_name = df["Autor"].values[0]
    st.title(author_display_name)
    # Show events for the author
    df_search = df_events.loc[df_events["author_clean_name"] == author_clean_name, :].reset_index()
    # Show the cards
    N_cards_per_col = 5
    for n_row, row in df_search.iterrows():
        i = n_row%N_cards_per_col
        if i==0:
            st.write("")
            cols = st.columns(N_cards_per_col, gap="large")
        create_card(row, cols[n_row%N_cards_per_col])
    add_color_to_cards()
    # Show social media for the author
    companies_list = ["twitter", "linkedin", "github"]
    known_companies_html = []
    for company in companies_list:
        if company in df.columns:
            link = df[company].values[0]
            image_link = f"https://cdn-icons-png.flaticon.com/512/124/124021.png"
            html = clickable_image_html(link, image_link, style="width:2%;")
            known_companies_html.append(html)
    cols = st.columns(len(companies_list))
    for i, html in enumerate(known_companies_html):
        with cols[i]:
            st.components.v1.html(html)
    # Show table!
    st.write(df)
    # Return button
    if st.button("Volver a la página principal"):
        st.experimental_set_query_params()

def display_404_author(author):
    """
    """
    st.title("404")
    st.write(f"No se encontró el autor {author} entre los autores registrados.")
    if st.button("Volver a la página principal"):
        st.experimental_set_query_params()