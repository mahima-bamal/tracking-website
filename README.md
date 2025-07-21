Social Pulse
Overview
Social Pulse is an AI-powered web application designed to address the challenge faced by brand teams in tracking real-time content from influencers and competitors across multiple platforms. By monitoring a curated list of verified YouTube, Instagram, and LinkedIn accounts, Social Pulse summarizes recent content, identifies trends, and delivers actionable insights through a trend brief generated when the user clicks the "Summarize" button.
Features

Account Verification: Validates and curates a list of verified influencer and competitor accounts on YouTube, Instagram, and LinkedIn.
Content Summarization: Summarizes posts and videos from the past 48 hours using the Gemini API.
Trend Analysis & Recommendations: Analyzes trends in the niche and provides actionable recommendations to help brands stay competitive.
Trend Brief Generation: Generates and sends a comprehensive trend brief to the brand team upon clicking the "Summarize" button, using SMTPlib for email delivery.
User-Friendly Interface: Built with Streamlit for an intuitive and interactive user experience.
Data Validation: Utilizes Pydantic for robust data modeling and validation.

Tech Stack

Gemini API: Powers content summarization and trend analysis.
Instagram Graph API: Fetches verified Instagram account data and posts.
YouTube Data API: Retrieves verified YouTube channel data and recent videos.
LinkedIn API: Pulls content from verified LinkedIn accounts.
Streamlit: Provides a web-based interface for user interaction.
SMTPlib: Handles email delivery of trend briefs.
Pydantic: Ensures data integrity and validation for API responses and user inputs.

How It Works

Input Handles: Users provide YouTube handles, Instagram IDs, and LinkedIn account details of influencers or competitors.
Verification: Social Pulse verifies the accounts to ensure they are valid and authentic.
Content Fetching: The system pulls posts and videos from the past 48 hours using the Instagram Graph API, YouTube Data API, and LinkedIn API.
Summarization & Analysis: Upon clicking the "Summarize" button, the Gemini API processes the fetched content to generate summaries, identify trends, and provide recommendations.
Trend Brief Delivery: The trend brief with insights and recommendations is emailed to the brand team using SMTPlib when the "Summarize" button is clicked.
User Interaction: Users interact with the Streamlit interface to input accounts and trigger summarization.

Why Use Social Pulse?

Real-Time Insights: Stay updated on what influencers and competitors are posting in your niche.
Actionable Recommendations: Leverage AI-driven trend analysis to make informed strategic decisions.
Efficient Workflow: Generate concise trend briefs on-demand with a single click.
Scalable Monitoring: Easily track multiple verified accounts across platforms.
User-Friendly: Intuitive interface makes it accessible for brand teams of all technical levels.

Installation

Clone the repository:
git clone https://github.com/your-username/social-pulse.git


Navigate to the project directory:
cd social-pulse


Install dependencies:
pip install -r requirements.txt


Set up environment variables for API keys and SMTP credentials in a .env file:
YOUTUBE_DATA_API_KEY=your_youtube_data_api_key
LINKEDIN_API_KEY=your_linkedin_api_key
GEMINI_API_KEY=your_gemini_api_key
IG_USER_ID=your_instagram_user_id
APP_ID=your_instagram_app_id
APP_SECRET=your_instagram_app_secret
USER_ACCESS_TOKEN=your_instagram_user_access_token
LONG_ACCESS_TOKEN=your_instagram_long_lived_access_token
SENDER_EMAIL_ID=your_email
SENDER_EMAIL_ID_PASSWORD=your_email_password


Run the Streamlit app:
streamlit run app.py



Usage

Access the web interface via the provided Streamlit URL (e.g., http://localhost:8501).
Input verified YouTube handles, Instagram IDs, and LinkedIn account details of influencers or competitors.
Click the "Summarize" button to generate and view summarized content, trend analysis, and recommendations.
Receive the trend brief via email upon clicking the "Summarize" button.

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.
