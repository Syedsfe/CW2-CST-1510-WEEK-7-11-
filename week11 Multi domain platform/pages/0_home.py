import streamlit as st

st.set_page_config(page_title="Multi-Domain Intelligence Platform", layout="wide")

# LOGIN CHECK — redirect if logged in
if "logged_in" in st.session_state and st.session_state.logged_in:
    st.success(f"Welcome back, {st.session_state.username}!")
    st.info("Use the left sidebar to navigate across all intelligence domains.")
else:
    st.title("🔐 Multi-Domain Intelligence Platform")
    st.caption("Please log in using the **Login** page in the sidebar to access all features.")

st.divider()

st.header("📡 System Overview")
st.write("""
This platform integrates three intelligence domains:

### 🛡 Cybersecurity Intelligence
- Manage cyber incidents  
- View analytics dashboards  
- Ask the AI Cyber Analyst for insights  

### 📊 Data Science Intelligence  
- Manage dataset metadata  
- Explore analytics and trends  
- Talk to the Data Scientist AI Assistant  

### 🖥 IT Operations Intelligence  
- Track and manage IT support tickets  
- Analyze operational performance  
- Get help from the IT Ops AI Assistant  

Use the sidebar to navigate between domains once logged in.
""")

st.markdown("---")

st.subheader("ℹ️ Instructions")
st.write("""
1. Go to **Login** page and authenticate.  
2. Once logged in, you will automatically gain sidebar access to:  
   - Cybersecurity  
   - Data Science  
   - IT Operations  
   - AI Assistant  
3. Use the **Logout** button in the Login page when needed.
""")

st.markdown("---")
st.caption("Built as part of CST1510 — Week 11 OOP Refactoring Workshop")
