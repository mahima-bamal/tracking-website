import streamlit as st
import sqlite3

def dashboard():
    #page config
    # st.set_page_config(page_title="Tracking Dashboard", page_icon="📊")

    if st.button("Back to Home", key="dashboard_back"): # Back button
        st.session_state["page"] = "home"
        st.rerun()

    #session check
    username = st.session_state.get("username")
    if not username:
        st.error("You must be logged in to view this page.")
        return

    #DB connection
    with sqlite3.connect("users.db", check_same_thread=False) as conn:
        cursor = conn.cursor()

        # Fetch user data
        try:
            cursor.execute("SELECT youtube_id, instagram_id, email FROM users WHERE username=?", (username,))
            user_data = cursor.fetchone()

            if not user_data:
                st.warning("No user data found.")
                return
            
            youtube_id, instagram_id, email = user_data

        except sqlite3.Error as e:
            st.error(f"Database error: {e}")
            return
    
    # Display user data
    st.title("Your Social Media Profiles")
    st.subheader(f"Welcome, {username}!")
    st.markdown(f"**YouTube Handle:** {youtube_id if youtube_id else 'Not provided'}")
    st.markdown(f"**Instagram ID:** {instagram_id if instagram_id else 'Not provided'}")
    st.markdown(f"**Email:** {email if email else 'Not provided'}")

