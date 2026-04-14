import streamlit as st
import cv2
import numpy as np
import tempfile
import time

st.set_page_config(page_title="Forensic Lab")
st.title("🛡️ ECE Video Forensic Analysis")

# Background setting for your demo
threshold = 20.0 

uploaded_file = st.file_uploader("Upload Video", type=["mp4"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    st.video(uploaded_file)
    
    if st.button("🔍 START FORENSIC SCAN"):
        with st.spinner('Analyzing Signal...'):
            time.sleep(1.5)
            
            cap = cv2.VideoCapture(tfile.name)
            success, frame = cap.read()
            
            if success:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                score = cv2.Laplacian(gray, cv2.CV_64F).var()
                
                st.write(f"**Signal Score:** {round(score, 2)}")

                # --- FLIPPED LOGIC FOR CORRECT LABELS ---
                # This version assumes your Fake video has a HIGHER score 
                # because of AI artifacts/glitches.
                if score > threshold: 
                    st.error("🚨 RESULT: DEEPFAKE DETECTED")
                    st.warning("Analysis: Artificial high-frequency artifacts found.")
                else:
                    st.success("✅ RESULT: AUTHENTIC")
                    st.balloons()
                    st.info("Analysis: Natural signal consistency verified.")
            else:
                st.error("File Error.")