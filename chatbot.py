# chatbot.py
"""
Streamlit chatbot with different personas and memory
file saved as chatbot.py
"""
""" streamlit run chatbot.py run in terminal window, opens the local host"""

import os # to interact with the windows operating system
import time #to add delay
import streamlit as st #streamlit libraries for building simple web apps on python
from dotenv import load_dotenv #loads dot env variables from a .env file into environment created
from openai import OpenAI #imports openai's python pkg so that the complete script can talk with openai's API


load_dotenv() #reads .env file in same folder
API_KEY = os.getenv("OPENAI_API_KEY") #reads a variable openai_api_key. if exists, stored as API_KEY

if not API_KEY:
    st.error("OPENAI_API_KEY is not found. Put it in a .env file in THIS folder.") #error when API_KEY missing or empty
    st.stop() #stops further running of code without an API key being present

client = OpenAI(api_key=API_KEY) #this will create an open AI API client
#this client is used to send requests to and communicate openai service




PERSONAS = {
    "Neutral": "A polite helpful chat bot, gives clear and crisp/concise answers",
    "RoastBot": (
        "RoastBot. Sarcastic, clever and witty answers"
        "Only playful, no abusive or hateful content. "
        "short, humorous and snarky."
    ),
    "ShakespeareBot": (
        "ShakespeareBot. Answers in early modern english. "
        "poetic phrasing, anarchaic words, clear answers but shakespeare-like."
    ),
    "Emoji Translator": (
        "Emoji translator. Convert user's input to emojis or sequence of emojis. "
        "Preserve the message meaning but use only emojis and short phrases."
    ),

}


# Streamlit layout

st.set_page_config(page_title="ACM Task ChatBot", page_icon="🐈‍⬛") #can use only emojis or text as page icon, sets page name, and icon
st.title("ACM Task 1 — ChatBot with Memory And Personas")
st.markdown(
    "Chat runs continuously without any reruns. Choose a persona and start a conversation "
    "and the bot will reply while keeping conversation memory."
)

with st.sidebar: #st.slidebar tells streamlit to put all the controls into the left sidebar
    st.header("SETTINGS") #Shows small header in side bar
    persona = st.selectbox("Choose persona", list(PERSONAS.keys())) #creates dropdown with persona choices. when we select a persona it is stored in the variable called persona.
    max_tokens = st.slider("Maximum response length", min_value=50, max_value=800, value=300, step=50)#gives max length the AI's answer can be (max tokens = max length)
    temperature = st.slider("Degree of creativity", min_value=0.0, max_value=1.2, value=0.7, step=0.1)#slider to control the creativity of ai, more temperature meaning more creative
    clear_button = st.button("Clear all memory")#button clears all memory when pressed

    st.markdown("NOTE - You can use: \n`/persona <name>` : to switch persona mid-chat.\n-`quit` / `exit` / `bye` : to close chat input")
#markdown shows a small note aboutthe details about the personas and stuff

#keeps msgs across reruns

if "history" not in st.session_state:#place to stor data when web app is open, if no history, empty list created
    # history will be a list of dicts with {role, content}, role is user content is the text
    st.session_state.history = []

# Clear memory if asked
if clear_button:
    st.session_state.history = []#sets history as empty list
    st.rerun()#updates UI by rerunning everything

# If persona changed, we will NOT wipe memory automatically becaus ewe keep the past context.




def build_messages(persona_name: str, history: list):#builds msgs length to send to api
    #form of persona:chat history

    system_prompt = PERSONAS.get(persona_name, PERSONAS["Neutral"])
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    return messages

def get_bot_reply(messages, max_tokens=300, temperature=0.7):#Call OpenAI chat completion API and return the assistant text
    try:
        response = client.chat.completions.create( #calls openai chat completon with the following params
            model="gpt-4o-mini",   # lightweight chat model
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        # extract assistant text
        text = response.choices[0].message.content #AI reply text is found inside the response. We return that text
        return text
    except Exception as e: #f something goes wrong we return an error message instead of crashing.
        return f"[Error getting reply: {e}]"

def render_chat(history):

    for entry in history:
        role = entry["role"]
        content = entry["content"]
        if role == "user":
            st.markdown(f"**You:** {content}")
        else:
            st.markdown(f"**Chatbot:** {content}")


# chat input area

st.markdown("### Conversation")
chat_container = st.container()

with chat_container:
    if len(st.session_state.history) == 0:
        st.info("get started with the chatbot! type your first message to start the chat..")

    render_chat(st.session_state.history)# Renders current conversation

    # auto clear option exists
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("You:", placeholder="Type your message here")
        submit = st.form_submit_button("Send")

    # for switchingbetween the different personaas
    if user_input and user_input.strip().lower().startswith("/persona "):
        new_persona = user_input.strip()[9:].strip()
        if new_persona in PERSONAS:
            persona = new_persona
            st.success(f"Persona switched to: {persona}")
        else:
            st.error(f"No persona named '{new_persona}'. Available: {', '.join(PERSONAS.keys())}")
        st.rerun()

    # normal msg sending wrks
    if submit and user_input:
        if user_input.strip().lower() in ("quit", "exit", "bye"):
            st.session_state.history.append(
                {"role": "assistant", "content": "Bye! If you want to chat again, send a new message."}
            )
            st.rerun()

        # adds the users msg
        st.session_state.history.append({"role": "user", "content": user_input})

        # Call calls openai
        messages_for_api = build_messages(persona, st.session_state.history)
        with st.spinner("Chatbot is typing..."):
            bot_text = get_bot_reply(messages_for_api, max_tokens=max_tokens, temperature=temperature)

        # bots reply is added
        st.session_state.history.append({"role": "assistant", "content": bot_text})
        st.rerun()

    #submits only if send button or enter button pressed
    if submit and user_input:
        #all exit words can be used to end convo
        if user_input.strip().lower() in ("quit", "exit", "bye"):
            st.session_state.history.append({"role": "assistant", "content": "Bye! If you want to chat again, send a new message."})
            st.session_state.user_input = ""
            st.rerun()

        # my user's chat text will be appended to history
        st.session_state.history.append({"role": "user", "content": user_input})

        # builds messages for api
        messages_for_api = build_messages(persona, st.session_state.history)

        # gets a reply
        with st.spinner("Chatbot is typing..."):
            bot_text = get_bot_reply(messages_for_api, max_tokens=max_tokens, temperature=temperature)

        # this appends bot chat history and reruns so that ui gets updated
        st.session_state.history.append({"role": "assistant", "content": bot_text})
        st.session_state.user_input = ""  # clears the input box
        st.rerun()


# footer and save convo button:

if st.button("Download conversation as text"):
    # for plain text export plain-text export
    lines = []
    for e in st.session_state.history:
        prefix = "You: " if e["role"] == "user" else "Chatbot: "
        lines.append(prefix + e["content"])
    txt = "\n\n".join(lines)
    st.download_button("Click to download .txt", txt, file_name="conversation.txt", mime="text/plain")

st.caption("Made for ACM Task 1 — keeps memory, supports personas, and runs as a single python file.")
