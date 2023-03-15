import streamlit as st
import pandas as pd 
from myopenai import Gpt, sidebar_api_input
from pydub import AudioSegment
import openai
from audiorecorder import audiorecorder
from pydub import AudioSegment
import io
# https://medium.com/@avra42/build-your-own-chatbot-with-openai-gpt-3-and-streamlit-6f1330876846


# File preference 
##############################################################################################################
st.set_page_config(layout='wide', 
                   page_title='Chat',
                   page_icon='🤖')


# Check if API key is valid
sidebar_api_input()

if st.session_state.api_valid and 'gpt' not in st.session_state:
    st.session_state.gpt = Gpt()
    # openai.api_key = st.secrets['OPENAI_API_KEY']


 


# Start of the design
##############################################################################################################
### MAIN AREA
##############################################################################################################
st.title('Chat GPT')
st.write('A chatbot powered by OpenAI GPT-3.5 Turbo.')







# GAME AREA BELOW
##############################################################################################################
st.markdown("<hr style='height:1px;border:none;color:#FFA500;background-color:#FFA500;' /> ", unsafe_allow_html=True)
general_col1, general_col2 = st.columns([16, 3])


# Model Parameters 
with general_col2:
    st.write(' ') #This an dnext are to allign the button with the text area
    st.write(' ')
    with st.expander('Parameters'):
        # input1, input2, input3 = st.columns([1, 1, 1])
        n_answers = st.slider('Answers to generate', 
                              min_value=1, max_value=10, value=1, step=1,
                              help='How many chat completion choices to generate for each input message.\nWhen selecting multiple answers, all answers will be displayed at the same time which may take more time to load.\nIt\'s recommended to select the number of answers you want to see before asking the chatbot a question.'
                                )
        temperature = st.slider('Temperature', 
                                    min_value=0.0, max_value=2.0, value=1.0, step=.01,
                                    help='Higher values like 0.8 will make the output more random\nwhile lower values like 0.2 will make it more focused and deterministic.\nWe generally recommend altering this or `top_p` but not both.'
                                    )
        
        params = {
            'temperature': temperature,
            # 'top_p': 1,
            'n': 1,
            'stream': True,
            # 'max_tokens': 100,
            # 'presence_penalty': 0,
            # 'frequency_penalty': 0,
        }



# MIC
    audio = audiorecorder("Click to record", "Recording...")
    transcript = ''
    if len(audio) > 0:
        AudioSegment.from_file(io.BytesIO(audio.tobytes())).export('output_microphone.mp3', format='mp3')
        audio_file = open("output_microphone.mp3", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)['text']

# TEXT INPUT
with general_col1:
    label = "Talk to chat - For technical reasons, you can't send twice the same message but adding a space somewhere fixes it." 
    prompt = '' # modify later
    value = transcript if transcript != '' else prompt
    user_input = st.text_area(label, key='text_area', value=value)





chat_conversation = st.empty()
if user_input not in ('', st.session_state.gpt.past_question): 

    # st.write(user_input)
    st.session_state.gpt.add_message('user', user_input)
    st.session_state.gpt.past_message = user_input
    with st.spinner('Asking Chat...'):
        response = st.session_state.gpt.ask(params)
    
    # if params['stream']: 
    with general_col1:
        collected_messages = []
        chat_message = st.empty()            
        for index, chunk in enumerate(response):
            chat_message.empty()
            chunk_message = chunk['choices'][0]['delta']  
            collected_messages.append(chunk_message) 

            reply = ''.join([m.get('content', '') for m in collected_messages])
            # chat_message.caption(f'Chat:')
            chat_message.write(reply)
            # chat_message.markdown("<hr style='height:1px;border:none;color:#FFFFFF;background-color:#FFFFFF;' /> ", unsafe_allow_html=True)

        chat_message.empty()
        # data = {'role': ['user']
        #         'content': [message_content]
        #         'datetime': [datetime.now()]
        #         }
 
    # else: 
    #     #add response to all messages and display all 
    #     reply 
    #     st.session_state.gpt.save_response(response)



    st.session_state.gpt.add_message('assistant', reply)


    for message_index, message in enumerate(st.session_state.gpt.messages[::-1]):
        message_content = message['content']
        
        with general_col1:
            who = {'user': 'Me', 'assistant': 'Chat'}[message['role']]
            st.caption(f'{who}:')
            st.write(message_content)
            st.markdown("<hr style='height:1px;border:none;color:#FFFFFF;background-color:#FFFFFF;' /> ", unsafe_allow_html=True)