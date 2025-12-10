import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def datasci_ai_chat_ui():
    st.write("### 💬 Data Science Expert AI Chat")

    # Initialize history
    if "ds_ai_history" not in st.session_state:
        st.session_state.ds_ai_history = []

    # Show conversation
    for msg in st.session_state.ds_ai_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    user_input = st.chat_input("Ask the Data Science AI...")

    if user_input:
        st.session_state.ds_ai_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            full_reply = ""
            placeholder = st.empty()

            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a Senior Data Scientist specializing in machine learning, "
                            "statistics, data analysis, feature engineering, Python, pandas, "
                            "and visualization. Provide detailed, clear explanations and code examples."
                        )
                    },
                    {"role": "user", "content": user_input}
                ],
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_reply += chunk.choices[0].delta.content
                    placeholder.write(full_reply)

            st.session_state.ds_ai_history.append(
                {"role": "assistant", "content": full_reply}
            )