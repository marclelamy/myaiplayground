import streamlit as st
import os
import pandas as pd 
from myopenai import Gpt
import json
import toml 

# https://medium.com/@avra42/build-your-own-chatbot-with-openai-gpt-3-and-streamlit-6f1330876846

# File preference 
##############################################################################################################
st.set_page_config(layout='wide', 
                   page_title='MyPlayground',
                   page_icon='🤖')




# Start of the design
##############################################################################################################
### SIDEBAR




### MAIN AREA
##############################################################################################################
st.title('Welcome to My AI Playground!')
col1, col2, col3 = st.columns([7, 1, 2])
col1.write('''This is the ultimate destination for anyone who wants to explore and play with the latest Artificial Intelligence (AI) models. If you're curious about what AI is all about, but don't know where to start, you've come to the right place! Our platform is designed to break down the barriers between everyday tech enthusiasts and the often-confusing world of AI.

Our goal is simple: to provide easy access to the most popular and exciting AI models available, including models like GPT-3, ChatGPT and Dalle. Using one page per model, we allow you to tweak the parameters and experience the full range of these models' capabilities with the model parameters. 
We also want non techincal poeple and folks not working in AI to understand those models better. What they are, how they are made etc. That's why every model has a learning page where we explain the model and how it works and another page where you can play with it.

With MyPlayground.ai, you don't need extensive knowledge of AI or programming languages to dive into this exciting world. All you have to do is sign up, select a model, and start exploring its possibilities and uses. You can also clone the [Github](https://github.com/marclelamy/ChatPyGPT) repo and run it by yourself. You can also go in the settings and enter your API key if you have one. 

Whether you're a student, a business owner, or a tech enthusiast, our AI models will provide you with a unique and fun way to interact with cutting-edge technology.''')
           
col3.write('Author: Marc Lamy - [Github](https://github.com/marclelamy/myaiplayground)/[Linkedin](https://www.linkedin.com/in/marc-lamy/)')





st.subheader('Mission')
st.write('''
My Ai Playground has for mission to put the latest models and most performing models in the hands of non tech folks to break the technical barrier. 

We want to make AI accessible to everyone. We want to make AIs easy to use and combine them as much as we can to build a fun environment.
''')




st.subheader('Available models')
models_available =  {'Type': ['Image', 'Chat', 'Speech to Text'],
 'Company': ['OpenAI', 'OpenAI', 'OpenAI'],
 'Name ': ['DALL·E', 'gpt-3.5-turbo', 'whisper-1'],
 'Price': ['1024×1024 $0.020 / image 512×512 $0.018 / image 256×256 $0.016 / image', '$0.002 / 1K tokens', '0.006 / minute']}

models_available = pd.DataFrame(models_available)
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.table(models_available)

# Set up API KEY
##############################################################################################################
if 'OPENAI_API_KEY' in st.secrets:
   st.session_state['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
else: 
    st.session_state['OPENAI_API_KEY'] = ''



