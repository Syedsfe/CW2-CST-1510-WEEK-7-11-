import streamlit as st
import pandas as pd
from services.ai_assistant import AIAssistant
from services.database_manager import DatabaseManager

# PAGE CONFIG
st.set_page_config(page_title="AI Incident Analysis", layout="wide")

# LOGIN GUARD
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in to access the AI assistant.")
    st.stop()

# PAGE TITLE
st.title("🤖 AI Cyber Incident Analysis")
st.caption("Select a cybersecurity incident and let the AI perform structured analysis.")

st.divider()

# DATABASE
db = DatabaseManager("database/intelligence_platform.db")

# LOAD INCIDENTS
query = "SELECT id, title, severity, status, date FROM cyber_incidents"
rows = db.fetch_all(query)

if not rows:
    st.error("No cybersecurity incidents found in the database.")
    st.stop()

df = pd.DataFrame(rows, columns=["id", "title", "severity", "status", "date"])

# DROPDOWN LABEL
df["label"] = df.apply(
    lambda row: f"{row['id']} | {row['title']} ({row['severity']})",
    axis=1
)

# USER SELECTS INCIDENT
incident_label = st.selectbox("Select an incident to analyze:", df["label"].tolist())
incident_id = int(incident_label.split("|")[0].strip())

selected = df[df["id"] == incident_id].iloc[0]

# DISPLAY INCIDENT DETAILS
st.subheader("📄 Incident Details")
st.write(selected)

incident_text = (
    f"Incident ID: {selected['id']}\n"
    f"Title: {selected['title']}\n"
    f"Severity: {selected['severity']}\n"
    f"Status: {selected['status']}\n"
    f"Date: {selected['date']}\n"
)

st.divider()

# CREATE OOP AI INSTANCE
if "analysis_ai" not in st.session_state:
    st.session_state.analysis_ai = AIAssistant(
        "You are a cybersecurity analyst. Provide analysis in four structured sections:"
        "\n1. Root Cause Analysis"
        "\n2. Immediate Actions"
        "\n3. Prevention Measures"
        "\n4. Risk Assessment"
        "\nReturn your analysis in clear markdown format."
    )

ai = st.session_state.analysis_ai

# ANALYSIS PROMPT
prompt = f"""
Analyze this cybersecurity incident and provide four sections:

Incident Details:
- Title: {selected['title']}
- Severity: {selected['severity']}
- Status: {selected['status']}
- Date: {selected['date']}

Return analysis using markdown headings:

## 🔍 Root Cause Analysis
...

## 🚑 Immediate Actions
- ...

## 🛡 Prevention Measures
- ...

## ⚠ Risk Assessment
...
"""

# AI BUTTON
st.subheader("🤖 AI Analysis")

if st.button("Analyze Incident"):
    with st.chat_message("assistant"):
        reply = ai.send_message(prompt)
        st.markdown(reply)

    st.success("AI analysis complete.")
