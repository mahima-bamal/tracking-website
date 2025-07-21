import os
import requests
from datetime import datetime, timedelta
from dateutil import parser, tz
from dotenv import load_dotenv
import json
import google.generativeai as genai
from pydantic import BaseModel

# Load environment variables
load_dotenv()
ig_user_id = os.getenv("ig_user_id")
long_access_token = os.getenv("long_access_token")

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv("gemini_api_key"))
except Exception as e:
    print(f"Error configuring Gemini API: {str(e)}")
    exit(1)

# Define Pydantic model for response
class Response(BaseModel):
    instagram_trend: str
    instagram_recommend: str

def get_post_uploaded_instagram(ig_username):
    """
    Fetch recent Instagram posts for a given username within the last 48 hours.
    Returns a list of dictionaries with caption, likes, and timestamp.
    """
    if not ig_user_id or not long_access_token:
        print("Error: Instagram user ID or access token not set in .env file")
        return []

    required_parameter = "{media{caption,timestamp,like_count}}"
    url = (
        f"https://graph.facebook.com/v17.0/{ig_user_id}"
        f"?fields=business_discovery.username({ig_username}){required_parameter}"
        f"&access_token={long_access_token}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        metadata = response.json()

        # Check for API errors
        if "error" in metadata:
            print(f"Instagram API error: {metadata['error']['message']}")
            return []

        # Safely access media data
        media_data = metadata.get("business_discovery", {}).get("media", {}).get("data", [])
        if not media_data:
            print(f"No posts found for Instagram username: {ig_username}")
            return []

        current_time = datetime.now(tz.tzutc())
        forty_eight_hours_ago = current_time - timedelta(hours=48)
        caption_dict = []
        for media_item in media_data:
            try:
                timestamp = parser.parse(media_item.get("timestamp", ""))
                if timestamp >= forty_eight_hours_ago:
                    caption_dict.append({
                        "caption": media_item.get("caption", "No caption"),
                        "likes": media_item.get("like_count", 0),
                        "timestamp": media_item.get("timestamp", "No timestamp")
                    })
            except ValueError as e:
                print(f"Error parsing timestamp for post: {str(e)}")
                continue

        return caption_dict

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Instagram posts for {ig_username}: {str(e)}")
        return []
    except Exception as e:
        print(f"Unexpected error in get_post_uploaded_instagram: {str(e)}")
        return []

def gemini_model_insta(insta_detail):
    """
    Analyze Instagram posts and return trends and recommendations.
    """
    try:
        formatted_content = "\n".join([f"Caption: {item['caption']}\nLikes: {item['likes']}" for item in insta_detail])
        if not formatted_content:
            print("No Instagram data to analyze")
            return None

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.5
            },
            system_instruction=(
                "You are an AI agent designed to analyze social media data across multiple users. Based on the provided Instagram post captions and likes, "
                "analyze the trends and provide recommendations to succeed in the trend. Return a JSON response with 'instagram_trend' (string) and 'instagram_recommend' (string)."
            )
        )
        return model.generate_content(formatted_content)
    except Exception as e:
        print(f"Error in gemini_model_insta: {str(e)}")
        return None

def test_instagram_api():
    """
    Test the Instagram API by fetching posts for a given username.
    """
    test_username = "nasa"  # Replace with a valid Instagram Business/Creator account
    print(f"Testing Instagram API for username: {test_username}")
    
    posts = get_post_uploaded_instagram(test_username)
    if posts:
        print(f"Found {len(posts)} posts from the last 48 hours:")
        for post in posts:
            print(f"Caption: {post['caption']}")
            print(f"Likes: {post['likes']}")
            print(f"Timestamp: {post.get('timestamp', 'No timestamp available')}")
            print("-" * 50)
    else:
        print(f"No posts found or an error occurred for {test_username}")

# Run the test
if __name__ == "__main__":
    test_instagram_api()