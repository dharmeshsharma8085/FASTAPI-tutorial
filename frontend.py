import streamlit as st
import requests

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Gemini AI Chat",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #0e1117;
    }

    /* Header */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Chat messages */
    .user-message {
        background: #1f2937;
        padding: 14px 18px;
        border-radius: 18px;
        margin: 10px 0;
        margin-left: 20%;
    }

    .bot-message {
        background: #172033;
        padding: 14px 18px;
        border-radius: 18px;
        margin: 10px 0;
        margin-right: 20%;
    }

    .message-label {
        font-size: 12px;
        color: #9ca3af;
        margin-bottom: 5px;
    }

    /* Input */
    .stChatInput {
        padding-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">🤖 Gemini AI Chat</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Powered by Gemini + FastAPI</div>',
    unsafe_allow_html=True
)


# -----------------------------
# FastAPI URL
# -----------------------------
API_URL = "http://127.0.0.1:8000/chat"


# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Display Previous Messages
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Ask Gemini anything...")


if prompt:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI
    try:

        with st.chat_message("assistant"):

            with st.spinner("Gemini is thinking..."):

                response = requests.post(
                    API_URL,
                    json={
                        "message": prompt
                    },
                    timeout=60
                )

                if response.status_code == 200:

                    data = response.json()

                    answer = data["response"]

                    st.markdown(answer)

                    # Save assistant response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ FastAPI server is not running. "
            "Please start it using: uvicorn main:app --reload"
        )

    except requests.exceptions.Timeout:

        st.error(
            "⏳ Gemini took too long to respond."
        )

    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("⚙️ Settings")

    st.markdown("---")

    st.write("### 🚀 Backend")

    st.code(
        "http://127.0.0.1:8000",
        language="text"
    )

    st.write("### 🧠 Model")

    st.info("Gemini 2.5 Flash")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    st.caption(
        "Built with Streamlit + FastAPI + Gemini"
    )