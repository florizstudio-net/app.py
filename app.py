import os
import time
import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Video Prompt Extractor", page_icon="🎬", layout="centered")

st.title("🎬 AI Video Prompt Extractor")
st.write("Upload a video and automatically generate a detailed master prompt using AI!")

# Configured API Key
API_KEY = "AQ.Ab8RN6IP0YOsITVVbFDePNDc-ywtNqt8ANK6vfVtr085cDlStA"

if not API_KEY:
    st.error("Please provide a valid Gemini API Key.")
else:
    genai.configure(api_key=API_KEY)
    
    # Video Uploader Section
    uploaded_file = st.file_uploader("Upload a video file (MP4, MOV, AVI)", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        # Show file details (Name and Size)
        file_details = {"File Name": uploaded_file.name, "File Size": f"{uploaded_file.size / (1024 * 1024):.2f} MB"}
        st.write("📁 **File Details:**")
        st.json(file_details)

        # Simulated Upload Progress Bar for better UX
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
            status_text.text(f"Uploading... {percent_complete + 1}%")
            
        status_text.text("Upload Complete!")
        st.video(uploaded_file)
        
        if st.button("EXTRACT MASTER PROMPT"):
            with st.spinner("Analyzing video with Gemini, please wait..."):
                try:
                    # Save uploaded file temporarily
                    video_path = "temp_video.mp4"
                    with open(video_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    st.write("Processing file with AI...")
                    video_file = genai.upload_file(path=video_path)

                    # Call Gemini Model
                    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
                    
                    prompt = """
                    Analyze this video thoroughly. Based on the visuals, camera movements, lighting, subject, 
                    art style, and atmosphere, write a highly detailed 'Master Prompt' that can be used in 
                    AI video generators like Sora, Runway Gen-3, Kling, or Luma Dream Machine. 
                    Provide only the prompt clearly.
                    """

                    response = model.generate_content([video_file, prompt])

                    # Display Generated Prompt
                    st.success("Master Prompt generated successfully!")
                    st.subheader("Your Master Prompt:")
                    st.code(response.text, language="markdown")

                    # Remove temporary file
                    if os.path.exists(video_path):
                        os.remove(video_path)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
