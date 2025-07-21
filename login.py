import streamlit as st
import sqlite3
import hashlib
from app import valid_user_yt, valid_user_insta, valid_email #import verification functions

# DB setup
def init_db():
    with sqlite3.connect("users.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            youtube_id TEXT,            
            instagram_id TEXT,
            email TEXT NOT NULL
            )""")
        conn.commit()

init_db()  # Initialize the database

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest() # Hashing passwords for security

def login(): 
    # st.set_page_config(page_title="Login Page", page_icon="🔐") 
    st.title("Sign Up/Login")
    option = st.radio("Choose an option:", ("Login", "Sign Up"))
    
    # Login inputs
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Sign Up":
        # Social inputs
        youtube = st.text_input("YouTube Channel ID")
        insta = st.text_input("Instagram ID")
        email = st.text_input("Email ID(required)") 

        if st.button("Submit"): 
            # Check for empty fields
            if not username:
                st.error("Username is required.")
                return
            if not password:
                st.error("Password is required.")
                return
            if not email:
                st.error("Email ID is required.")
                return

            hashed_password = hash_password(password) # Hash the password before storing

            #Validate social media IDs
            if youtube and not valid_user_yt(youtube):
                st.error("Invalid Youtube Channel ID.")
                return
            if insta and not valid_user_insta(insta):
                st.error("Invalid Instagram ID.")
                return
            #validate email 
            if email and not valid_email(email):
                st.error("Invalid Email ID.")
                return
            try:
                with sqlite3.connect("users.db", check_same_thread=False) as conn:
                    cursor = conn.cursor() # Insert new user into the database
                    cursor.execute("INSERT INTO users (username, password, youtube_id, instagram_id, email) VALUES (?, ?, ?, ?, ?)",
                        (username, hashed_password, youtube if youtube else None, insta if insta else None, email if email else None))
                    conn.commit() #save changes
                    st.success("Account created successfully!")
                    st.session_state["logged_in"] = True # Store login state
                    st.session_state["username"] = username # Store username in session state
                    st.session_state["page"] = "home" # Store username in session state
                    st.rerun() # Reload the app
            except sqlite3.IntegrityError:
                st.error("Username already exists. Please choose a different username.")

    elif option == "Login":
        if st.button("Login"):
            hashed_password = hash_password(password)
            with sqlite3.connect("users.db", check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
                user = cursor.fetchone() # Fetch user data
                if user:
                    st.session_state["logged_in"] = True # Store login state
                    st.session_state["username"] = username # Store username in session state
                    st.session_state["page"] = "home"
                    st.session_state["show_login_message"] = True  # Show login message
                    st.rerun() # Reload the app
           
                else:
                    st.error("Invalid username or password.")
# conn.close() # even tho it closes the database connection, # Removed to avoid closing the connection at module level
