import streamlit as st
import requests
# Backend API URL (Replace with your deployed FastAPI URL)
API_URL = "http://127.0.0.1:8000/get_lesson"  # Change to your deployed API URL if needed

# Streamlit UI
st.set_page_config(page_title="AI Lesson Planner", layout="wide")

st.title("🎓 AI Lesson Planner")
st.write("Enter a YouTube Video ID, and our AI will generate a structured lesson.")

# Input field for YouTube video ID
video_id = st.text_input("Enter YouTube Video ID:", "")
st.image('yt_video-id.png')
if st.button("Generate Lesson"):
    if video_id:
        st.info("Generating lesson... Please wait.")
        
        # Send request to FastAPI backend
        response = requests.post(API_URL, json={"video_id": video_id})

        if response.status_code == 200:
            lesson_data = response.json()
            st.success("Lesson Generated Successfully! 🎉")
            
            # Display Lesson Content
            st.subheader("📖 Lesson")
            print(lesson_data.get("Lesson"))
            st.markdown(lesson_data.get("Lesson"))


        else:
            st.error("Failed to generate lesson. Please try again.")

    else:
        st.warning("Please enter a YouTube video ID.")

