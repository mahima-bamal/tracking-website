import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from dateutil import parser, tz
from pydantic import BaseModel
import google.generativeai as genai
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv("gemini_api_key"))
except Exception as e:
    print(f"Error configuring Gemini API: {str(e)}")
    exit(1)

# Define Pydantic model for response
class Response(BaseModel):
    youtube_trend: str
    youtube_recommend: str

# YouTube API setup
youtube_api_key = os.getenv("youtube_data_api")
if not youtube_api_key:
    print("Error: YouTube API key not found in .env file")
    exit(1)

try:
    youtube = build("youtube", "v3", developerKey=youtube_api_key)
except Exception as e:
    print(f"Error initializing YouTube API: {str(e)}")
    exit(1)

def get_video_uploaded_youtube(handle):
    try:
        current_time = datetime.now(tz.tzutc())
        forty_eight_hours_ago = current_time - timedelta(hours=48)

        # Get channel details
        request = youtube.channels().list(
            part="contentDetails",
            forHandle=handle
        )
        response = request.execute()

        if not response.get("items"):
            print(f"No channel found for handle: {handle}")
            return {}

        channel_id = response["items"][0]["id"]

        # Get uploads playlist ID
        request = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        response = request.execute()
        
        # Safely access uploads playlist
        uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"].get("uploads")
        if not uploads_playlist_id:
            print(f"No uploads playlist found for channel: {handle}")
            return {}

        # Get recent videos
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=50
        )
        response = request.execute()

        video_dict = {}
        for item in response.get("items", []):
            published_at = parser.parse(item["snippet"]["publishedAt"])
            if published_at >= forty_eight_hours_ago:
                title = item["snippet"]["title"]
                video_description = item["snippet"].get("description", "No description available")
                video_dict[title] = video_description
            else:
                break

        return video_dict

    except HttpError as e:
        print(f"YouTube API error for handle {handle}: {str(e)}")
        return {}
    except Exception as e:
        print(f"Error fetching YouTube videos for handle {handle}: {str(e)}")
        return {}

def gemini_model_youtube(video_details):
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.5
            },
            system_instruction=(
                "You are an AI agent designed to analyze social media data across multiple users. Based on the provided YouTube video titles and descriptions, "
                "analyze the trends and provide recommendations to succeed in the trend. Return a JSON response with 'youtube_trend' (string) and 'youtube_recommend' (string)."
            )
        )
        return model.generate_content(video_details)
    except Exception as e:
        print(f"Error initializing Gemini model: {str(e)}")
        return None
'''
# Fetch videos and generate content
handle = "@GaugingGadgets"
get_video = get_video_uploaded_youtube(handle)
if not get_video:
    print(f"No recent videos found for {handle}")
else:
    video_content = "\n".join([f"Title: {title}\nDescription: {description}" for title, description in get_video.items()])
    response = gemini_model_youtube(video_content)
    
    if response:
        try:
            response_json = json.loads(response.text)
            # Validate with Pydantic model
            validated_response = Response(**response_json)
            print({
                "youtube_trend": validated_response.youtube_trend,
                "youtube_recommend": validated_response.youtube_recommend
            })
        except json.JSONDecodeError as e:
            print(f"Error parsing Gemini response as JSON: {str(e)}")
        except ValueError as e:
            print(f"Invalid response format from Gemini: {str(e)}")
    else:
        print("No response from Gemini model")
'''