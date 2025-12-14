import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


class AIAssistant:
    """
    A reusable AI assistant class that manages:
    - Chat history
    - System prompt
    - OpenAI API calls
    - Streaming responses
    """

    def __init__(self, system_prompt: str):
        # Load API key (from secrets.toml or environment)
        api_key = (
            st.secrets.get("OPENAI_API_KEY")
            if "OPENAI_API_KEY" in st.secrets
            else os.getenv("OPENAI_API_KEY")
        )

        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in secrets.toml or environment variables.")

        # Create OpenAI client
        self._client = OpenAI(api_key=api_key)

        # Store system prompt & initialize chat history
        self._system_prompt = system_prompt
        self._history = [{"role": "system", "content": self._system_prompt}]

    # ----------------------------------------------------------------------
    # SEND MESSAGE (WITH STREAMING)
    # ----------------------------------------------------------------------
    def send_message(self, user_message: str):
        """
        Sends a message to the AI, streams the response live in Streamlit,
        saves history, and returns the full assistant reply.
        """

        # Add user message to history
        self._history.append({"role": "user", "content": user_message})

        # Placeholder for streaming output
        placeholder = st.empty()
        full_reply = ""

        # Request streaming response from OpenAI
        stream = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self._history,
            stream=True
        )

        # Streaming loop
        for chunk in stream:
            if (
                chunk.choices
                and chunk.choices[0].delta
                and chunk.choices[0].delta.content
            ):
                full_reply += chunk.choices[0].delta.content
                placeholder.write(full_reply)

        # Save assistant's reply to history
        self._history.append({"role": "assistant", "content": full_reply})

        return full_reply

    # ----------------------------------------------------------------------
    # GET CHAT HISTORY
    # ----------------------------------------------------------------------
    def get_history(self):
        return self._history

    # ----------------------------------------------------------------------
    # CLEAR CHAT HISTORY
    # ----------------------------------------------------------------------
    def clear_history(self):
        self._history = [{"role": "system", "content": self._system_prompt}]
