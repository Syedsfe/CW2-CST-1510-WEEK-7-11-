import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def itops_ai_chat_ui():
    st.write("### 💬 IT Operations AI Chat")

    # Initialize chat history
    if "it_ai_history" not in st.session_state:
        st.session_state.it_ai_history = []

    # Display chat history
    for msg in st.session_state.it_ai_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    user_input = st.chat_input("Ask the IT Ops AI...")

    if user_input:
        st.session_state.it_ai_history.append({"role": "user", "content": user_input})
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
                            "You are an IT Operations Engineer specializing in troubleshooting, "
                            "networks, system performance, server issues, DevOps, automation, "
                            "and incident resolution. Provide practical, step-by-step solutions."
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

            st.session_state.it_ai_history.append(
                {"role": "assistant", "content": full_reply}
            )