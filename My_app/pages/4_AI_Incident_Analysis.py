import streamlit as st
from openai import OpenAI
from database import DatabaseManager
import pandas as pd
from dotenv import load_dotenv
import os 

#AUTH GUARD
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to access AI incident analysis.")
    st.stop()

#OPENAI CLIENT
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
client=OpenAI(api_key=api_key)

#DATABASE MANAGER
db = DatabaseManager()

#PAGE HEADER
st.title("AI Cyber Incident Analysis")
st.caption("Select a cybersecurity incident from the database and let AI analyze it.")

st.divider()

# 1. LOAD INCIDENT DATA FROM DB

query = "SELECT * FROM cyber_incidents"
rows = db.fetch_all(query)

if not rows:
    st.error("No cyber incidents found in the database.")
    st.stop()

# Convert rows to DataFrame
columns = ["id", "title", "severity", "status", "date",]
df = pd.DataFrame(rows, columns=columns)

#Ccreating readable dropdown labels 
df["label"]=df.apply(lambda row: F"{row['id']} | {row['title']} ({row['severity']})", axis=1)
# 2.Selection of the incident 

incident_label= st.selectbox(
    "Select an incident to analyze:",
    df["label"].tolist()
)

incident_id = int(incident_label.split("|")[0].strip())  # extract ID
selected = df[df["id"] == incident_id].iloc[0]

# Displaying Incident DETAILS
st.subheader("Incident Details")
st.write(selected)

#Prepare text for AI
incident_text = (
    f"Incident ID: {selected['id']}\n"
    f"Date: {selected['date']}\n"
    f"Title: {selected['title']}\n"
    f"Status: {selected['status']}"
    f"Severity: {selected['severity']}"
)

st.divider()

# 3. SENDING INCIDENT TO AI
st.divider()
st.subheader("AI Analysis")

prompt = f"""
Analyze this cybersecurity incident and return **FOUR separate sections**.

Incident Details:
- Title: {selected['title']}
- Severity: {selected['severity']}
- Status: {selected['status']}
- Date: {selected['date']}

Return the analysis in this EXACT JSON format (no extra text):

{{
  "root_cause": "...",
  "immediate_actions": ["...", "...", "..."],
  "prevention_measures": ["...", "...", "..."],
  "risk_assessment": "..."
}}
"""
if st.button("Analyze with AI"):
    st.subheader("AI Analysis")

    placeholder = st.empty()
    full_output = ""

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": 
                "You are a cybersecurity analyst. Provide analysis in this format:\n"
                "1. Root Cause Analysis\n"
                "2. Immediate Actions\n"
                "3. Prevention Measures\n"
                "4. Risk Assessment\n"
                "Use bullet points and emojis exactly like the PPT."
            },
            {
                "role": "user",
                "content": f"Analyze the following cybersecurity incident:\n\n{incident_text}"
            }
        ],
        stream=True,
    )

    # STREAMING LOOP 
    for chunk in stream:
        if chunk.choices[0].delta.content:
            full_output += chunk.choices[0].delta.content
            placeholder.markdown(full_output)

    st.success("AI analysis complete.")