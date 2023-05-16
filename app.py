#####################
# Import Libs
#####################

import os
import sys

import requests

import numpy as np
import pandas as pd
import matplotlib

import streamlit as st
from streamlit_chat import message

import openai

from langchain.agents import create_csv_agent, create_pandas_dataframe_agent
from langchain.llms import OpenAI


#####################
# Streamlit Settings
#####################

# Hide traceback
st.set_option('client.showErrorDetails', False)

# Setting page title and header
st.set_page_config(page_title="Query CSV with ChatGPT", page_icon=":bar_chart:")
st.markdown("<h1 style='text-align: center;'>Quering a dataset with ChatGPT</h1>", unsafe_allow_html=True)

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

#####################
# OpenAI API Key
#####################

# My OpenAI API key is in a file called 'ram_openai_apikey.txt', 
# in the home project dir
key_filename = 'ram_openai_apikey.txt'

def get_apikey_from_file(filename):
    """ Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

# Get the API Key from file and set the env vble
openai_api_key = get_apikey_from_file(key_filename)
openai.api_key = openai_api_key
os.environ["OPENAI_API_KEY"] = openai_api_key

# Check if the API key is valid 
try:
      models = openai.Model.list()
except Exception as e:
      st.error("Error testing API key: {}".format(e))


#####################
# CSV File Upload
#####################

# Allow user to upload CSV file
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Read uploaded file as a Pandas DataFrame
    dataframe = pd.read_csv(uploaded_file)
    # Visualize the data table
    st.write(dataframe)
    
    data_quality_check = st.checkbox('Request Data Quality Check')


    #####################
    # Data Quality Check
    #####################
    if data_quality_check:
        st.write("The following data quality analysis has been made")
        st.markdown("**1. The dataset column names have been checked for trailing spaces**")
        trailing_spaces = dataframe.columns[dataframe.columns.str.contains("\s+$", regex=True)]
        if trailing_spaces.empty:
            st.markdown('*Columns_ names_ are_ found_ ok*')
        else:
            st.markdown("*Columns with trailing spaces:* ")
            st.write(f"{', '.join(trailing_spaces)}")

        # Check data type of columns with name 'date'
        st.markdown("**2. The dataset's date columns have been checked for the correct data type**")
        date_cols = dataframe.select_dtypes(include="object").filter(regex="(?i)date").columns
        for col in date_cols:
            if pd.to_datetime(dataframe[col], errors="coerce").isna().sum() > 0:
                st.write("Column {col} should contain dates but has wrong data type")
            else:
                st.write("Columns with date are of the correct data type")


#########################
# Responses from df Agent
#########################

# Define a function to generate response from user input
# Using LangChain pandas df agent
def generate_response(input_text):
    agent = create_pandas_dataframe_agent(OpenAI(temperature=0), dataframe, verbose=False)
    query_response = agent.run(input_text)
    return query_response


#########################
# Chat UI
#########################

# container for chat history
response_container = st.container()

# container for text box
input_container = st.container()

with input_container:
    # Create a form for user input
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Submit')

    if submit_button and user_input:
        # If user submits input, generate response and store input and response in session state variables
        try:
            query_response = generate_response(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(query_response)
        except Exception as e:
            st.error("An error occurred: {}".format(e))

if st.session_state['generated']:
    # Display chat history in a container
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
