import streamlit as st
from services.ai_assistant import AIAssistant

def itops_ai_chat_ui():

    # Create the AI assistant only once
    if "it_ai" not in st.session_state:
        st.session_state.it_ai = AIAssistant(
            "You are an IT Operations Engineer specializing in troubleshooting, "
            "networks, system performance, server issues, DevOps, automation, "
            "and incident resolution. Provide simple explanations when needed, "
            "and step-by-step solutions."
        )

    ai = st.session_state.it_ai

    st.write("### 💬 IT Operations AI Chat")

    # Display chat history
    for msg in ai.get_history()[1:]:   # Skip system message
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    user_input = st.chat_input("Ask the IT Ops AI...")

    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.write(user_input)

        # Get assistant reply via OOP service class
        reply = ai.send_message(user_input)

        # Display assistant message
        with st.chat_message("assistant"):
            st.write(reply)
