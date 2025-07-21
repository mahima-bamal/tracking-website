import streamlit as st

def home():
    username = st.session_state.get("username") # Get username from session state
    if not username: #check if user is logged in
        st.error("You must be logged in to view this page.") 
        return
    
    st.title(f"Welcome, {username}!") 
    st.header("See the Play, Seize the Day")
    st.write("Explore your social media insights below. Choose an option to View Your Social Media Profiles or analyze the latest trends and win them through our recommendation")
    
    col1, col2 = st.columns(2)
    with col1: 
        if st.button("View Your Social Media Profiles", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
    with col2:
        if st.button("View Trend Analysis And Recommendation", use_container_width=True):
            st.session_state["page"] = "trend_analysis"
            st.rerun()

    if st.button("Logout", key="home_logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["page"] = "login"
        st.session_state["show_login_message"] = False  # Reset login message flag
        st.rerun()
