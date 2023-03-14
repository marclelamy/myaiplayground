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

 


# Start of the design
##############################################################################################################
### MAIN AREA
##############################################################################################################
st.title('Chat GPT')
# st.markdown(check_openai_api_key(st.secrets['OPENAI_API_KEY'])[0])


col1, col2, col3 = st.columns([4, 4, 2])
col1.write('A chatbot powered by OpenAI GPT-3.5 Turbo.')


### TABS 
##############################################################################################################
# tab1, tab2 = st.tabs([, "Play"])


# with tab2: 
    # st.write('Learn about the model')
    # st.markdown('''

    # What to add to learning page: 
    # * What is GPT 
    # * What is NLP 
    # * How to build it from scratch? Karparthy video 

    # ''')
    # st.title("The following list won’t indent no matter what I try:")
    # st.header('The following list won’t indent no matter what I try:')
    # st.subheader('The following list won’t indent no matter what I try:')
    # st.write('The following list won’t indent no matter what I try:')
    # st.markdown('The following list won’t indent no matter what I try:')
    # st.code('print("The following list won’t indent no matter what I try:")', language='python')


##############################################################################################################
# THIS IS WHERE PLAYING STARTS
##############################################################################################################
# with tab2: 
if st.button('Clear'):
    for key in st.session_state.keys():
        if key not in ('OPENAI_API_KEY'):
            del st.session_state[key]
        
        if key == 'gpt': 
            st.session_state.gpt = Gpt(st.secrets['OPENAI_API_KEY'])

# st.write(st.session_state)


### SIDEBAR
##############################################################################################################
sidebar_api_input()

if 'gpt' not in st.session_state:
    st.session_state.gpt = Gpt(st.secrets['OPENAI_API_KEY'])
if 'user_input' not in st.session_state:
    st.session_state.user_input = ''
if 'show_message_index' not in st.session_state:
    st.session_state.gpt.show_message_index = []

st.session_state.gpt.messages = []
for _ in range(3):
    st.write(' ')






# Prompts Parameters
############################################################################################################## 
input1, input2, input3 = st.expander('Parameters').columns([1, 1, 1])
df_prompts = pd.read_csv('data/prompts.csv')
df_prompts.loc[len(df_prompts)] = ['None', '']
df_prompts.loc[len(df_prompts)] = ['', '']

### Prompt selecton
test_area_prompt = input1.selectbox(
        "Chose a prompt for the chatbot to 'act as'",
        [''] + df_prompts['act_as'].sort_values().tolist())
test_area_prompt = '' if test_area_prompt == 'None' else test_area_prompt
prompt = df_prompts[df_prompts['act_as'] == test_area_prompt].iloc[0, 1] + ''
# input1.write(prompt + ' The more detailed you can be, the better.')






### Model Parameters
##############################################################################################################
n_answers = input2.slider('How many answers do you want?', 
                        min_value=1, 
                        max_value=10, 
                        value=1, 
                        step=1,
                        help='The number of answers you want to get from the chatbot.\nWhen selecting multiple answers, all answers will be displayed at the same time which may take more time to load.\nIt\'s recommended to select the number of answers you want to see before asking the chatbot a question.'
                        )
st.session_state.gpt.n_answers = n_answers
temperature = input3.slider('what temperature do you want?', 
                            min_value=0.0, 
                            max_value=2.0, 
                            value=1.0, 
                            step=.01,
                            help='The temperature of the chatbot. The higher the temperature, the more creative the answers will be.'
                            )
st.session_state.gpt.temperature = temperature






# INPUT AREA
##############################################################################################################
col1, col2 = st.columns([16, 3])

# COST
prompt_cost = round(st.session_state.gpt.num_tokens_from_string(st.session_state.user_input, 'gpt-3.5-turbo') / 1000 * 0.002, 5)
# col2.write(prompt_cost)
col2.write(' ')
with col2:
    audio = audiorecorder("Click to record", "Recording...")
    transcript = ''
    if len(audio) > 0:
        byte_audio = audio.tobytes()
        # Export the AudioSegment to a WAV file
        AudioSegment.from_file(io.BytesIO(byte_audio)).export('output_microphone.mp3', format='mp3')
        audio_file = open("output_microphone.mp3", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)['text']


# TEXT INPUT
value = transcript if transcript != '' else prompt
label = "Talk to chat - For technical reasons, you can't send twice the same message but adding a space somewhere fixes it." 
st.session_state.user_input = col1.text_area(label, key='text_area', value=value)








# Create conversation container
if 'conversation_chat_container' not in st.session_state:
    st.session_state.conversation_chat_container = st.empty()


# Make the request and display chat
##############################################################################################################
if st.session_state.user_input not in ('', test_area_prompt, prompt, st.session_state.gpt.past_question):
    st.session_state.gpt.add_user_input(st.session_state.user_input)

    # Loop to get one answer per iteration
    for nn in range(n_answers):
        with st.session_state.conversation_chat_container.container():
            # Make the request
            print('Making the request...')
            with st.spinner('Asking Chat...'):
                st.session_state.gpt.show_message_index += [1]
                st.session_state.gpt.ask(st.session_state.user_input)

            col_user, col_messages, col_checkbox = st.columns([5, 2, 2])
            # Display conversation
            person = {'user': 'Me', 'assistant': 'Chat'}
            for message_index, message in enumerate(st.session_state.gpt.messages[::-1]):
                message_content = message['content']
                
                with col_user:
                    who = person[message['role']]
                    st.caption(f'{who}:')
                    st.write(message_content)
                    st.markdown("<hr style='height:1px;border:none;color:#FFFFFF;background-color:#FFFFFF;' /> ", unsafe_allow_html=True)


            # Display answer
            # print(f'{st.session_state.gpt.show_message_index = } - last line')

# Write a cringe LinkedIn post about how I'm so excited about using chat GPT and whisper through their API in a streamlit web app.


