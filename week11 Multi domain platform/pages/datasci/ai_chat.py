import streamlit as st
from services.ai_assistant import AIAssistant

def datasci_ai_chat_ui():

    # Create AI assistant instance only once
    if "ds_ai" not in st.session_state:
        st.session_state.ds_ai = AIAssistant(
            "You are a Senior Data Scientist specializing in machine learning, "
            "statistics, data analysis, pandas, Python, and visualization. "
            "Provide detailed answers with examples when needed."
        )

    ai = st.session_state.ds_ai

    st.write("### 💬 Data Science Expert AI Chat")

    # Display previous messages
    for msg in ai.get_history()[1:]:     # skip system prompt
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    user_input = st.chat_input("Ask the Data Science AI...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        # Get AI response from service class
        reply = ai.send_message(user_input)

        with st.chat_message("assistant"):
            st.write(reply)
