import streamlit as st
from dotenv import load_dotenv
load_dotenv()   ## Load all the environment variables
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are the Youtube Video summarizer. You will take the transcript text and summarize the 
entire video, providing the important voice in points within 250 words. The transcript is appended here: """

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

def extract_transcript_detail(youtube_video_link):
    try:
        video_id = youtube_video_link.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e

# Set page configuration
st.set_page_config(
    page_title="YouTube Transcript Converter",
    page_icon=":movie_camera:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Set background color with texture
st.markdown(
    """
    <style>
        body {
            background-color: #FFE4B5;
            background-image: url('https://www.google.com/url?sa=i&url=https%3A%2F%2Ftechandall.com%2F10-blur-wallpapers-backgrounds-for-your-website%2F&psig=AOvVaw0U1mv-SGVRB120KITsGjSc&ust=1708489814087000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCNibwYSKuYQDFQAAAAAdAAAAABAQ');  /* Replace with your texture image URL */
            color: #FFFFFF;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add YouTube search input and button
st.title("YouTube Transcript to Detailed Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_detail(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
