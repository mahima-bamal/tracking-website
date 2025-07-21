# Social Pulse

## Overview
Social Pulse is an AI-powered web application designed to address the challenge faced by brand teams in tracking real-time content from influencers and competitors across multiple platforms. By monitoring a curated list of verified YouTube, Instagram, and LinkedIn accounts, Social Pulse summarizes recent content, identifies trends, and delivers actionable insights through a trend brief generated when the user clicks the "Summarize" button.

## Features
- **Account Verification**: Validates and curates a list of verified influencer and competitor accounts on YouTube, Instagram, and LinkedIn.
- **Content Summarization**: Summarizes posts and videos from the past 48 hours using the Gemini API.
- **Trend Analysis & Recommendations**: Analyzes trends in the niche and provides actionable recommendations to help brands stay competitive.
- **Trend Brief Generation**: Generates and sends a comprehensive trend brief to the brand team upon clicking the "Summarize" button, using SMTPlib for email delivery.
- **User-Friendly Interface**: Built with Streamlit for an intuitive and interactive user experience.
- **Data Validation**: Utilizes Pydantic for robust data modeling and validation.

## Tech Stack
- **Gemini API**: Powers content summarization and trend analysis.
- **Instagram Graph API**: Fetches verified Instagram account data and posts.
- **YouTube Data API**: Retrieves verified YouTube channel data and recent videos.
- **LinkedIn API**: Pulls content from verified LinkedIn accounts.
- **Streamlit**: Provides a web-based interface for user interaction.
- **SMTPlib**: Handles email delivery of trend briefs.
- **Pydantic**: Ensures data integrity and validation for API responses and user inputs.

## How It Works
1. **Input Handles**: Users provide YouTube handles, Instagram IDs, and LinkedIn account details of influencers or competitors.
2. **Verification**: Social Pulse verifies the accounts to ensure they are valid and authentic.
3. **Content Fetching**: The system pulls posts and videos from the past 48 hours using the Instagram Graph API, YouTube Data API, and LinkedIn API.
4. **Summarization & Analysis**: Upon clicking the "Summarize" button, the Gemini API processes the fetched content to generate summaries, identify trends, and provide recommendations.
5. **Trend Brief Delivery**: The trend brief with insights and recommendations is emailed to the brand team using SMTPlib when the "Summarize" button is clicked.
6. **User Interaction**: Users interact with the Streamlit interface to input accounts and trigger summarization.

## Why Use Social Pulse?
- **Real-Time Insights**: Stay updated on what influencers and competitors are posting in your niche.
- **Actionable Recommendations**: Leverage AI-driven trend analysis to make informed strategic decisions.
- **Efficient Workflow**: Generate concise trend briefs on-demand with a single click.
- **Scalable Monitoring**: Easily track multiple verified accounts across platforms.
- **User-Friendly**: Intuitive interface makes it accessible for brand teams of all technical levels.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/social-pulse.git
   ```
2. Navigate to the project directory:
   ```bash
   cd social-pulse
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables for API keys and SMTP credentials in a `.env` file:
   ```plaintext
   YOUTUBE_DATA_API_KEY=your_youtube_data_api_key
   LINKEDIN_API_KEY=your_linkedin_api_key
   GEMINI_API_KEY=your_gemini_api_key
   IG_USER_ID=your_instagram_user_id
   APP_ID=your_instagram_app_id
   APP_SECRET=your_instagram_app_secret
   USER_ACCESS_TOKEN=your_instagram_user_access_token
   SENDER_EMAIL_ID=your_email
   SENDER_EMAIL_ID_PASSWORD=your_email_password(google app password)
   ```
5. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Access the web interface via the provided Streamlit URL (e.g., `http://localhost:8501`).
2. Input verified YouTube handles, Instagram IDs, and LinkedIn account details of influencers or competitors.
3. Click the "Summarize" button to generate and view summarized content, trend analysis, and recommendations.
4. Receive the trend brief via email upon clicking the "Summarize" button.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.
