import streamlit as st
import json
import os
import time
from auto_email import send_auto_email
st.set_page_config(page_title="Social Pulse", page_icon="🤖")

from login import login
from home import home
from dashboard import dashboard
from app import trend_analysis

# Function to load competitor data (copied from test_app.py)
def load_data():
    DATA_FILE = "competitors.json"
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def main():
    #setup session on first load
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["show_login_message"] = False #flag for login msg
    if "page" not in st.session_state or st.session_state["page"] not in ["login", "home", "dashboard", "trend_analysis"]:
        st.session_state["page"] = "login"
    # Initialize competitors to avoid KeyError in trend_analysis
    if 'competitors' not in st.session_state:
        st.session_state.competitors = load_data() or [{} for _ in range(5)]    

        #show login sucess msg only once after login
        if st.session_state["page"] == "home" and st.session_state.get("show_login_message", False):
            placeholder = st.empty()
            with placeholder:
                st.success(f"Logged in as {st.session_state['username']}")
                time.sleep(4)
            placeholder.empty()
            st.session_state["show_login_message"] = False #prevent showing again

    if st.session_state["page"] == "login":
        login()
    elif st.session_state["page"] == "home":
        home()
    elif st.session_state["page"] == "dashboard":
        dashboard()
    elif st.session_state["page"] == "trend_analysis":
        trend_analysis()

if __name__ == "__main__":
    main()
    send_auto_email()
