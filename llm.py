"""
This uses Large Language Models to allow for a more flexible search engine.
We will use LangChain and OpenAI to search for the the most appropriate videos
(from the ones on the website) for a given query.
It should allow to answer questions like:
(Topic 1) Possible equivalent questions:
- Data Science
- What is data science?
- What is the best video to learn about data science?
(Topic 2) Possible equivalent questions:
- Machine Learning
- What is machine learning?
- What is the best video to learn about machine learning?
- What is forecasting?
- What is random forest?
(Topic 3) Possible equivalent questions:
- Streamlit
- What is streamlit?
- What is the best video to learn about streamlit?
"""

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

from helpers import get_events_data

def get_most_relevant_videos(user_query, df, openai_api_key):
    """
    This function takes a query and a dataframe and returns the indices of the
    most relevant videos in the dataframe for the query.
    """
    # Convert the dataframe to a markdown table only for columns of interest:
    # index, title, description, tags, author, and type
    df_md = df[["Titulo"]].to_csv()
    # Create a prompt template (this is not an f-string, but a template)
    prompt_template_str = """
    Using the table provided on markdown format, find the most relevant videos
    for the user query that will be provided below. 
    You must return a list of indices of the videos in the dataframe that are
    relevant to the query. Do not return more indices than are necessary or applicable.
    Do not return more than a maximum of 10 indices. 
    The list must be sorted and must be provided as a python list of integers. 
    The values of the integers must be the indices of the videos in the dataframe. 
    The output should be a python list of integers as a comma separated string, 
    from the most relavant to the least relevant. For example, if the most relevant
    video is the 12th, then the second most relevant is the 0th, then the third
    most relevant is the 4th, and the fourth most relevant is the 3rd, then the
    output should be:
    ```
    [12, 0, 4, 3]
    ```
    The query will be a text provided by the user, and will be delimited by triple simple 
    quotes like ```this```.

    Dataframe:
    {data}

    Query:
    ```
    {query}
    ```
    """

    prompt_template = ChatPromptTemplate.from_template(prompt_template_str)
    # Initialize the Large Language Model
    llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.0)
    # Create the prompt to be sent to the API
    query_prompt = prompt_template.format_messages(
                            data=df_md,
                            query=user_query)
    # Get the indexes (as a string)
    full_answer = llm(query_prompt)
    indexes_str = eval(full_answer.content)
    # Convert to python
    indexes_list = list(indexes_str)
    return indexes_list

if __name__=="__main__":
    import toml
    openai_api_key = toml.load(".streamlit/secrets.toml")["OPENAI_KEY"]
    # Here we mock the user query
    user_query = "data science"
    # Load the dataframe
    df = get_events_data()
    # Get the sorted list of indices of videos (relative to the dataframe)
    # that are the most relevant to the query
    indexes = get_most_relevant_videos(user_query, df, openai_api_key)
    # Filter the dataframe to only show the relevant videos
    df_search = df.loc[indexes]
    # Print the result
    print(df_search)


