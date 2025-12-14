import streamlit as st
from services.ai_assistant import AIAssistant

def cyber_ai_chat_ui():

    if "cyber_ai" not in st.session_state:
        st.session_state.cyber_ai = AIAssistant(
            "You are a Senior Cybersecurity Analyst. "
            "Provide accurate insights on threats, vulnerabilities, defences, "
            "attack vectors, and incident response strategies."
        )

    ai = st.session_state.cyber_ai

    st.write("### 💬 Cybersecurity Expert AI Chat")

    # Display conversation history
    for msg in ai.get_history()[1:]:   # skip system message
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User sends a message
    user_input = st.chat_input("Ask the cybersecurity AI...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        reply = ai.send_message(user_input)

        with st.chat_message("assistant"):
            st.write(reply)
