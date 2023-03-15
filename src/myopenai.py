from urllib import response
import openai 
import pandas as pd
import numpy as np
import sqlite3 
from datetime import datetime
import tiktoken
import streamlit as st
import base64
import os 
import json










def check_openai_api_key(api_key):
    '''
    Checks if the provided OpenAI API key is valid by attempting to list the available models.
    '''    
    openai.api_key = api_key
    try: 
        openai.Model.list()
        return "Openai API key is :green[working]", True
    except Exception as e:
        return f"Openai API key is :red[invalid or not working]: {e}", False

def sidebar_api_input(): 
    '''Displays a text input widget in the Streamlit sidebar for users to enter their OpenAI API key.
    If the key is already set in the Streamlit secrets, it will be used to check if the key is valid 
    using the `check_openai_api_key()` function.
    '''
    if 'OPENAI_API_KEY' not in st.secrets:
        st.secrets['OPENAI_API_KEY'] = ''
    if st.secrets['OPENAI_API_KEY'] == '':
        st.secrets['OPENAI_API_KEY'] = st.sidebar.text_input('Enter your OpenAI API Key to use the models. Find it [here](https://platform.openai.com/account/api-keys).')
    else: 
        message, valid = check_openai_api_key(st.secrets['OPENAI_API_KEY'])
        st.sidebar.markdown(message)


    if valid: 
        st.session_state['api_valid'] = True
        openai.api_key = st.secrets['OPENAI_API_KEY']








class Gpt(): 
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.messages = []
        self.past_question = ''
        self.conversation_id = np.random.randint(10**10)
    
    def add_message(self, role, message_content):
        message = {'role': role, 'content': message_content}
        self.messages.append(message)   

    # def log_message(self, role, message_content):
    #     data = {'role': [role]
    #             'content': [message_content]
    #             'datetime': [datetime.now()]
    #             }
        
    #     df = pd.DataFrame(data)


    def ask(self, params): 
        self.request_id = np.random.randint(10**10)
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-0301", 
            messages = self.messages,
            **params
            )
        
        return completion
    

    def save_response(self, response):
        if not os.path.exists('data/responses/'):
            os.mkdir('data/responses/')
        
        with open(f'data/responses/{self.conversation_id}_{self.request_id}.json', 'w') as f:
            response = json.dumps(response.to_dict())
