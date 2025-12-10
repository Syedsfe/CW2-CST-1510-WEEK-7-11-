import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def cyber_ai_chat_ui():
    st.write("### 💬 Cybersecurity Expert AI Chat")

    # Initialize chat history
    if "cyber_ai_history" not in st.session_state:
        st.session_state.cyber_ai_history = []

    # Display previous messages
    for msg in st.session_state.cyber_ai_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask the Cybersecurity AI...")

    if user_input:
        # Store and display user message
        st.session_state.cyber_ai_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # AI response (streaming)
        with st.chat_message("assistant"):
            full_reply = ""
            placeholder = st.empty()

            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a Senior Cybersecurity Analyst. "
                            "Provide accurate insights on threats, vulnerabilities, defenses, "
                            "attack vectors, and incident response strategies."
                        )
                    },
                    {"role": "user", "content": user_input}
                ],
                stream=True
            )

            # Build the response as it streams
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_reply += chunk.choices[0].delta.content
                    placeholder.write(full_reply)

            st.session_state.cyber_ai_history.append(
                {"role": "assistant", "content": full_reply}
            )