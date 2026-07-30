import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Video Prompt Extractor", page_icon="🎬", layout="centered")

st.title("🎬 AI Video Prompt Extractor")
st.write("একটি ভিডিও আপলোড করুন এবং এআই-এর সাহায্যে তার মাস্টার প্রম্পট তৈরি করে নিন!")

api_key = st.text_input("আপনার Google Gemini API Key দিন:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    uploaded_file = st.file_uploader("একটি ভিডিও ফাইল আপলোড করুন (MP4, MOV ইত্যাদি)", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("EXTRACT MASTER PROMPT"):
            with st.spinner("ভিডিও অ্যানালাইজ করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন..."):
                try:
                    video_path = "temp_video.mp4"
                    with open(video_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    st.write("ফাইল প্রসেস হচ্ছে...")
                    video_file = genai.upload_file(path=video_path)

                    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
                    
                    prompt = """
                    Analyze this video thoroughly. Based on the visuals, camera movements, lighting, subject, 
                    art style, and atmosphere, write a highly detailed 'Master Prompt' that can be used in 
                    AI video generators like Sora, Runway Gen-3, Kling, or Luma Dream Machine. 
                    Provide only the prompt clearly.
                    """

                    response = model.generate_content([video_file, prompt])

                    st.success("সফলভাবে মাস্টার প্রম্পট তৈরি হয়েছে!")
                    st.subheader("আপনার মাস্টার প্রম্পট:")
                    st.code(response.text, language="markdown")

                    if os.path.exists(video_path):
                        os.remove(video_path)

                except Exception as e:
                    st.error(e)
else:
    st.info("টুলটি ব্যবহার করতে প্রথমে ওপরে আপনার Gemini API Key দিন।")
  
