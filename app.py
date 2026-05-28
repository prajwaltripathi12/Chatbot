import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Ollama AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#4CAF50;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    height:3em;
}

.user-msg{
    padding:15px;
    border-radius:10px;
    background:#1E1E1E;
    margin-bottom:10px;
}

.bot-msg{
    padding:15px;
    border-radius:10px;
    background:#262730;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# ENV VARIABLES
# =====================================

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv(
    "LANGCHAIN_API_KEY"
)

os.environ["LANGCHAIN_TRACING_V2"] = "true"

os.environ["LANGCHAIN_PROJECT"] = (
    "Simple Q&A Chatbot With Ollama"
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# =====================================
# PROMPT
# =====================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant."
    ),
    
    MessagesPlaceholder(
        variable_name="chat_history"
    ),

    (
        "human",
        "{question}"
    )
])


# =====================================
# RESPONSE FUNCTION
# =====================================

def generate_response(
    question,
    engine,
    temperature,
    max_tokens
):

    llm = OllamaLLM(
        model=engine,
        temperature=temperature,
        num_predict=max_tokens
    )

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    # Convert session history
    history=[]

    for msg in st.session_state.messages:

        if msg["role"]=="user":
            history.append(
                HumanMessage(
                    content=msg["content"]
                )
            )

        else:
            history.append(
                AIMessage(
                    content=msg["content"]
                )
            )

    answer = chain.invoke(
        {
            "question":question,
            "chat_history":history
        }
    )

    return answer


# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages=[]


# =====================================
# HEADER
# =====================================

st.markdown(
    '<p class="title">🤖 Ollama AI Assistant</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Powered by LangChain + Ollama</p>',
    unsafe_allow_html=True
)


# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.header("⚙ Settings")

    llm=st.selectbox(
        "Select Model",
        [
            "mistral",
            "gemma2",
            "llama3"
        ]
    )

    temperature=st.slider(
        "Temperature",
        0.0,
        1.0,
        0.7
    )

    max_tokens=st.slider(
        "Max Tokens",
        50,
        1000,
        300
    )

    st.divider()

    st.info(
        f"""
        Model : {llm}

        Temperature : {temperature}

        Max Tokens : {max_tokens}
        """
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages=[]



# =====================================
# DISPLAY OLD MESSAGES
# =====================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )


# =====================================
# USER INPUT
# =====================================

user_input=st.chat_input(
    "Ask me anything..."
)

if user_input:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            response=generate_response(
                user_input,
                llm,
                temperature,
                max_tokens
            )

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":response
        }
    )