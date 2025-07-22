import streamlit as st
import os
import json
import smtplib
import sqlite3
from datetime import datetime
from dateutil import tz
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from instagram_graph_api import get_post_uploaded_instagram, gemini_model_insta
from youtube_data_api import get_video_uploaded_youtube, gemini_model_youtube
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
youtube_api_key = os.getenv("youtube_data_api")
ig_user_id = os.getenv("ig_user_id")
long_access_token = os.getenv("long_access_token")
app_id = os.getenv("app_id")
app_secret = os.getenv("app_secret")
user_access_token = os.getenv("user_access_token")
sender_email_id = os.getenv("sender_email_id")
sender_email_id_password = os.getenv("sender_email_id_password")

# YouTube API setup
try:
    youtube = build("youtube", "v3", developerKey=youtube_api_key)
except Exception as e:
    st.error(f"Error initializing YouTube API: {str(e)}")
    youtube = None

# Database setup
def init_db():
    with sqlite3.connect("competitors.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS competitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                username TEXT,
                youtube TEXT,
                instagram TEXT,
                verified BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES users(username)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT NOT NULL
            )
        """)
        conn.commit()

# Initialize database
init_db()

def valid_user_yt(handle):
    if not youtube:
        return False
    try:
        request = youtube.channels().list(
            part="id",
            forHandle=handle
        )
        response = request.execute()
        return bool(response.get("items"))
    except HttpError as e:
        st.error(f"YouTube API error: {str(e)}")
        return False
    except Exception:
        return False

def valid_user_insta(ig_username):
    if not ig_user_id or not long_access_token:
        return False
    required_parameter = "{media{caption,timestamp,like_count}}"
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}?fields=business_discovery.username({ig_username}){required_parameter}&access_token={long_access_token}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        metadata = response.json()
        return "business_discovery" in metadata and not metadata.get("error")
    except Exception:
        return False

def valid_email(email):
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender_email_id, sender_email_id_password)
        s.sendmail(sender_email_id, email, "email verified")
        s.quit()
        return True
    except:
        return False

# Load and save data functions
def load_data(user_id):
    try:
        with sqlite3.connect("competitors.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username, youtube, instagram, verified 
                FROM competitors 
                WHERE user_id = ?
            """, (user_id,))
            rows = cursor.fetchall()
            return [{"username": row[0], "youtube": row[1], "instagram": row[2], "verified": row[3]} for row in rows]
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return [{} for _ in range(4)]

def save_data(user_id, data):
    try:
        with sqlite3.connect("competitors.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM competitors WHERE user_id = ?", (user_id,))
            for item in data:
                cursor.execute("""
                    INSERT INTO competitors (user_id, username, youtube, instagram, verified)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id,
                    item.get('username', ''),
                    item.get('youtube', ''),
                    item.get('instagram', ''),
                    item.get('verified', False)
                ))
            conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")

# Initialize session state
if 'competitors' not in st.session_state:
    username = st.session_state.get("username", "default_user")  # Assume username is set during login
    st.session_state.competitors = load_data(username) or [{} for _ in range(4)]

def summarize_competitors(username):
    
    verified_youtube_handle = []
    verified_instagram_username = []
    data = load_data(username)
    for item in data:
        if item.get("verified") and item.get("youtube"):
            verified_youtube_handle.append(item["youtube"])
        if item.get("verified") and item.get("instagram"):
            verified_instagram_username.append(item["instagram"])

    # Process Instagram data
    summerized_insta_captionn_likes = []
    for ig_username in verified_instagram_username:
        if ig_username:
            try:
                posts = get_post_uploaded_instagram(ig_username)
                summerized_insta_captionn_likes.extend(posts)
            except Exception as e:
                st.error(f"Error fetching Instagram data for {ig_username}: {str(e)}")

    instagram_trend, instagram_recommend = "", ""
    if summerized_insta_captionn_likes:
        try:
            response = gemini_model_insta(summerized_insta_captionn_likes)
            if response:
                response_json = json.loads(response.text)
                instagram_trend = response_json.get("instagram_trend", "No trends available")
                instagram_recommend = response_json.get("instagram_recommend", "No recommendations available")
            else:
                st.error("No response from Gemini for Instagram data")
        except json.JSONDecodeError as e:
            st.error(f"Error parsing Instagram Gemini response: {str(e)}")
        except Exception as e:
            st.error(f"Error processing Instagram summary: {str(e)}")

    # Process YouTube data
    summerized_youtube_title_description = []
    for handle in verified_youtube_handle:
        if handle:
            try:
                get_yt_details = get_video_uploaded_youtube(handle)
                video_content = "\n".join([f"Title: {title}\nDescription: {description}" for title, description in get_yt_details.items()])
                summerized_youtube_title_description.append(video_content)
            except Exception as e:
                st.error(f"Error fetching YouTube data for {handle}: {str(e)}")

    youtube_trend, youtube_recommend = "", ""
    if summerized_youtube_title_description:
        try:
            response = gemini_model_youtube(summerized_youtube_title_description)
            if response:
                response_json = json.loads(response.text)
                youtube_trend = response_json.get("youtube_trend", "No trends available")
                youtube_recommend = response_json.get("youtube_recommend", "No recommendations available")
            else:
                st.error("No response from Gemini for YouTube data")
        except json.JSONDecodeError as e:
            st.error(f"Error parsing YouTube Gemini response: {str(e)}")
        except Exception as e:
            st.error(f"Error processing YouTube summary: {str(e)}")
    
    message = (
                    "<html><body>"
                    "<p>Here is the trend analysis with recommendations to win it:</p>"
                    "<p><b>Instagram Trends:</b><br>{instagram_trend}</p>"
                    "<p><b>Instagram Recommendations:</b><br>{instagram_recommend}</p>"
                    "<p><b>YouTube Trends:</b><br>{youtube_trend}</p>"
                    "<p><b>YouTube Recommendations:</b><br>{youtube_recommend}</p>"
                    "<p>Thank you for using our service.</p>"
                    "</body></html>"
                ).format(
                    instagram_trend=instagram_trend,
                    instagram_recommend=instagram_recommend,
                    youtube_trend=youtube_trend,
                    youtube_recommend=youtube_recommend
                )
    
    summary_date=datetime.now(tz.tzutc())
    with sqlite3.connect("users.db",check_same_thread=False) as conn:
        cursor=conn.cursor()
        cursor.execute("UPDATE users SET summary_date = ? WHERE username = ?", (summary_date, username))
        conn.commit()
    
    return message

def send_mail(username,message):
    # Fetch user's email from database
    receiver_email_id = None
    try:
        with sqlite3.connect("users.db", check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            if result:
                receiver_email_id = result[0]
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    # Send email with summary
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender_email_id, sender_email_id_password)
        msg = MIMEText(message, 'html')
        msg['Subject'] = "Competitor Trend Analysis Report"
        msg['From'] = sender_email_id
        msg['To'] = receiver_email_id
        s.send_message(msg)
        s.quit()
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
    return None

def trend_analysis():
    if st.button("Back to Home", key="trend_analysis_back"):
        st.session_state["page"] = "home"
        st.rerun()

    st.title("Manage Your Competitors Here")
    st.write("Enter details to track your competitors")

    username = st.session_state.get("username", "default_user")  # Get logged-in user's username

    # Function to handle verify button click
    def verified_row(row_index):
        st.session_state.competitors[row_index]['verified'] = True
        st.write(f"Verified for row {row_index + 1}: Processing data for {st.session_state.competitors[row_index].get('username', 'N/A')}...")
        save_data(username, st.session_state.competitors)

    # Display input fields
    for row in range(len(st.session_state.competitors)):
        with st.container():
            cols = st.columns([2, 2, 2, 2])
            with cols[0]:
                competitor_username = st.text_input('Username', key=f'username_{row}', value=st.session_state.competitors[row].get('username', ''))
                st.session_state.competitors[row]['username'] = competitor_username
            with cols[1]:
                youtube = st.text_input('YouTube Handle', key=f'youtube_{row}', value=st.session_state.competitors[row].get('youtube', ''))
            with cols[2]:
                instagram = st.text_input('Instagram', key=f'instagram_{row}', value=st.session_state.competitors[row].get('instagram', ''))
            with cols[3]:
                if st.button('Verify', key=f'verify_{row}', use_container_width=True):
                    with st.container():
                        if not youtube and not instagram:
                            st.session_state.competitors[row]['youtube'] = ""
                            st.session_state.competitors[row]['instagram'] = ""
                            save_data(username, st.session_state.competitors)
                            continue
                        
                        if youtube:
                            if not valid_user_yt(youtube):
                                st.warning(f"Row {row + 1}: Invalid YouTube handle '{youtube}'. Please enter a valid handle.")
                                st.session_state.competitors[row]['youtube'] = ''
                            else:
                                st.session_state.competitors[row]['youtube'] = youtube
                        else:
                            st.session_state.competitors[row]['youtube'] = ''
                        if instagram:
                            if not valid_user_insta(instagram):
                                st.warning(f"Row {row + 1}: Invalid Instagram handle '{instagram}'. Please enter a valid handle.")
                                st.session_state.competitors[row]['instagram'] = ''
                            else:
                                st.session_state.competitors[row]['instagram'] = instagram
                        else:
                            st.session_state.competitors[row]['instagram'] = ''
                        
                        if st.session_state.competitors[row].get('youtube') or st.session_state.competitors[row].get('instagram'):
                            verified_row(row)
                        else:
                            st.warning(f"Row {row + 1}: No valid handles provided. Verification skipped.")

    # Save data
    save_data(username, st.session_state.competitors)

    # Button to add new row
    if st.button("Add New Competitor"):
        st.session_state.competitors.append({})
        save_data(username, st.session_state.competitors)

    # Fetching Instagram long-lived access token
    try:
        url = f"https://graph.facebook.com/v17.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={user_access_token}"
        response = requests.get(url)
        response.raise_for_status()
        long_access_token = response.json().get("access_token")
    except requests.exceptions.HTTPError as e:
        long_access_token = None
    except Exception as e:
        long_access_token = None

    # Summarize button
    col1, col2, col3 = st.columns([0.1, 2, 0.1])
    with col2:
        if st.button("Summarize"):
            st.markdown("### Summary of Verified Competitors")
            message_summary=summarize_competitors(username)
            mail=send_mail(username,message_summary)
            st.success(f"Summary sent mail successfully!")
        else:
            st.write("No summary.")
