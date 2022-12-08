import streamlit as st

from helpers import *
from events import *
from authors import *

st.set_page_config(page_title="Contenido audiovisual Python Chile", page_icon="https://pythonchile.cl/images/favicon.png", 
                layout="wide", initial_sidebar_state="expanded")
df_events = get_events_data()
df_authors = get_authors_data()

# If query if for author, then show author page. If not, show events (search) page
query_params = st.experimental_get_query_params()
if "author" in query_params:
    author = query_params["author"][0]
    if is_author_in_authors:
        display_author(df_authors, df_events, author)
    else:
        display_404_author(author)
else:
    display_search(df_events)