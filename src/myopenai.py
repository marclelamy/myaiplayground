from urllib import response
import openai 
import pandas as pd
import numpy as np
import sqlite3 
import json
import os 
import requests
from datetime import datetime
import tiktoken
import streamlit as st
import base64

def check_openai_api_key(api_key):
    if api_key == '':
        return ":red[No Openai API key provided yet]", False
    openai.api_key = api_key
    try: 
        openai.Model.list()
        return "Openai API key is :green[working]", True
    except Exception as e:
        return f"Openai API key is :red[invalid or not working]: {e}", False


def input_api_key():
    # st.write(st.session_state)
    # if 'openai_api_key_input' in st.session_state:
    #     del st.session_state['openai_api_key_input']
    # st.write(st.session_state)
    st.session_state['OPENAI_API_KEY'] = st.sidebar.text_input('Enter your OpenAI API Key to use the models. Find it [here](https://platform.openai.com/account/api-keys).')
    # st.write(st.session_state)

def sidebar_api_input(): 
    # st.sidebar.write(st.session_state['OPENAI_API_KEY'])
    # st.sidebar.write('OPENAI_API_KEY' in st.session_state)
    # st.sidebar.write(st.session_state['OPENAI_API_KEY'] not in (None, ''))
    if 'OPENAI_API_KEY' not in st.session_state:
        st.session_state['OPENAI_API_KEY'] = ''
    if st.session_state['OPENAI_API_KEY'] == '':
        input_api_key()
    

    message, valid = check_openai_api_key(st.session_state['OPENAI_API_KEY'])
    st.sidebar.markdown(message)
    if valid == False and st.session_state['OPENAI_API_KEY'] != '':
        input_api_key()




# lst = [{"role": "user", "content": "So I've been worried an article about the app that I just made. So I'm currently making a streamlined application with a bunch of AI APIs. So I'm using chat GPT API, Dali API, Whisper API. So like those are different models for like text, image, and speech to text. And they also use stable diffusion, which is a model that takes text and image. And so I'm making, so like all those different tools are like on different websites, different platforms and stuff. And so what I'm doing is pretty much grouping everything into one single web app where people can just enter the API key and just start playing with all the APIs without having to do much else. They can also like store all their data locally. Everything is like when they start a session, there's a database that is created. And all the image generated also saved just like build your house. And so I want you to help me write an article about it. Propose me another line, maybe ask me more questions for clarification and I will answer" },
#   {"role": "assistant", "content": "Sure, I'd be happy to help you write an article about your new app. Can you tell me more about how users can benefit from this app? For example, in what ways can the AI APIs improve their work or daily tasks?" },
# {"role": "user", "content": "Well, for example, one thing could be, well, chat.jpg, it's the use, so that's great. Delijous screen image, that's fun. And then Whisper, you can translate any, for example, like audio, so like the audio of a video, for example. And then you can just extract Jojo and then just convert it into text, which is great, for example, for clouds or anything." },
# {"role": "assistant", "content": "That's really interesting! So, it sounds like your app can help users with various tasks, such as transcribing audio, recognizing images, and even analyzing text? How does your app streamline these processes compared to users manually accessing each API separately? Can you speak more to the ease of use that your app offers?" },
# {"role": "user", "content": "an article written by chat gpt after interviewing me by talking to it (with whisper) about the webapp that I made and from which I got interviewed." },
# {"role": "assistant", "content": "That's a unique idea! By interviewing you through the app, we can showcase the app's capability in real-time. We can then describe the conversation between you and the AI, highlighting the features and benefits of the app that you discuss. For this, I'm going to ask you multiple questions about the app and then write a full outline, is that okay?" }]
lst = []

class Gpt(): 
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.conversation_id = np.random.randint(10**12)
        self.messages = lst
        self.past_question = ''
        self.hide_message_map = []


    def add_user_input(self, message): 
        self.log_question(message)
        self.hide_message_map.append(1)
        message = {'role': 'user', 'content': message}
        if message != self.messages:
            self.messages.append(message)



    def ask(self, message):
        '''Ask a question to the model'''
        self.past_question = message
        response = self.request()
        chat_answer = []
        # print(response.keys())
        # for key in response.keys():
        #     print(key, response[key], '\n')
        # print(f'\n\n\n{response.keys() = }\n\n\n')
        for chat_message in response['choices']:
            # print(chat_message)
            message = chat_message['message']
            message['index'] = chat_message['index']
            self.messages.append(message)
            chat_answer.append(message['content'])

        self.log_answer(response)
        return chat_answer

    

    def request(self): 
        '''Makes a request to Open AI'''
        # print(self.message)
        # print('\n\n'*3)
        # for message in self.messages:
        #     print(message)

        messages = [{i:j for i, j in message.items() if i in ('role', 'content')} for index, message in enumerate(self.messages)]

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", 
            messages = messages,
            temperature = self.temperature,
            n = 1,
            # n = self.n_answers,
            )
        # print(completion.keys())
        return completion.to_dict()



    
    def new_conversation(self): 
        '''Reset some parameters like conversation id and stuff'''





    def log_question(self, message): 
        '''Add a message to the conversation'''
        self.con = sqlite3.connect('data/database.sqlite')
        pd.DataFrame({'content': [message], 'conversation_id': [self.conversation_id], 'datetime': [datetime.now()]}).to_sql('questions', self.con, if_exists='append', index=False)



    def log_answer(self, data): 
        '''Add a message to the conversation'''
        # st.write(data)
        # print(data)
        self.con = sqlite3.connect('data/database.sqlite')
        data.update(data['usage'])
        data.pop('usage')
        df_answers = pd.DataFrame(data['choices'])
        data.pop('choices')
        df_information = pd.DataFrame([data])
        df_information['conversation_id'] = self.conversation_id

        df_answers = pd.concat([df_answers, pd.json_normalize(df_answers['message'])], axis=1)
        df_answers = df_answers.drop('message', axis=1)
        df_answers['prompt_id'] = data['id']
        df_answers['conversation_id'] = self.conversation_id

        df_information.to_sql('information', self.con, if_exists='append', index=False)
        df_answers.to_sql('answers', self.con, if_exists='append', index=False)
        return df_answers


    def num_tokens_from_string(self, string: str, model_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
        num_tokens = len(encoding.encode(string))
        return num_tokens
    


class Dalle(): 
    def __init__(self, api_key=None):
        # self.set_api_key()
        self.api_key = api_key
        self.conversation_id = np.random.randint(10**12)
        self.con = sqlite3.connect('data/database.sqlite')
        self.messages = []
        self.past_question = ''



    def imagine (self, 
                 prompt, 
                 n_image,
                 image_size
                 ):
        
        self.requestID = np.random.randint(10**12)
        params = {
            'prompt': prompt,
            'n': n_image,
            'size': image_size,
            'response_format': 'b64_json'
            }
        
        self.log_params(params)
        response = self.request(params)
        self.log_response(response)
        return response
    

    def request(self, params): 
        return openai.Image.create(
                        params
                        )



    def log_params(self, params):
        self.con = sqlite3.connect('data/database.sqlite')
        df = pd.DataFrame([params])
        df['conversation_id'] = self.conversation_id
        df['request_id'] = self.requestID
        df.to_sql('dalle_params', self.con, if_exists='append', index=False)


    def log_response(self, response):
        self.con = sqlite3.connect('data/database.sqlite')
        
        data = {'created': [], 'image_data': [], 'index': []}
        for image_index, image_data in enumerate(response['data']):
            data['created'].append(response['created'])
            data['image_data'].append(image_data['b64_json'])
            data['index'].append(image_index + 1)
            data['conversation_id'] = self.conversation_id
            data['request_id'] = self.requestID

        pd.DataFrame(data).to_sql('dalle_response', self.con, if_exists='append', index=False)



    def responses_to_images(self, response): 
        images = []
        for index, image_data in enumerate(response['data']):
            image = base64.b64decode(image_data['b64_json'])
            with open(f'image_{index + 1}.png', 'wb') as f:
                f.write(image)


        return images



    # def download_image(self, image_url): 

    #     return image










class Whisper(): 
    def __init__(self, api_key=None):
        # self.set_api_key()
        self.api_key = api_key
        self.conversation_id = np.random.randint(10**12)
        self.con = sqlite3.connect('data/database.sqlite')
        self.messages = []
        self.past_question = ''



    def transcribe(self, message): 
        transcription = openai.Audio.transcribe(
            model = 'whisper-1',
            file="test_audio.mp3"
            )
