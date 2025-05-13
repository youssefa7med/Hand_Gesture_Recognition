import streamlit as st
import cv2
import face_recognition
import os
import json
import numpy as np
from pathlib import Path
from streamlit_lottie import st_lottie
from gtts import gTTS
from io import BytesIO
import pygame

# Initialize pygame mixer for audio
pygame.mixer.init()

def play_audio_message(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        st.error(f"Error in audio playback: {str(e)}")

st.set_page_config(page_title="Sign Up", layout="wide")

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        padding: 0.75rem 1rem;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        color: white;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .success-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #cce5ff;
        border: 1px solid #b8daff;
        color: #004085;
    }
    .stTextInput>div>div {
        border-radius: 10px;
    }
    .stSelectbox>div>div {
        border-radius: 10px;
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 2rem;
    }
    .input-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
root_dir = current_dir.parent
Login_Animation_file = current_dir.parent / "assets" / "Sign_up_Animation.json"
FACES_DIR = root_dir / "faces"

# Ensure directory exists
FACES_DIR.mkdir(exist_ok=True)

########################################################################################

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

########################################################################################

def load_registered_users():
    users = {}
    try:
        if os.path.exists(FACES_DIR):
            for file in os.listdir(FACES_DIR):
                if file.endswith(".json"):
                    with open(os.path.join(FACES_DIR, file), "r") as f:
                        user_data = json.load(f)
                        users[user_data['name']] = np.array(user_data['encoding'])
    except Exception as e:
        st.error(f"Error loading registered users: {str(e)}")
    return users

########################################################################################

def is_face_registered(face_encoding):
    try:
        registered_users = load_registered_users()
        for user, encoding in registered_users.items():
            matches = face_recognition.compare_faces([encoding], face_encoding)
            if any(matches):
                return True
    except Exception as e:
        st.error(f"Error checking face registration: {str(e)}")
    return False

########################################################################################

def register_user(camera_index, name, visa_number, expiration_month, expiration_year, cvv):
    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            st.error("📷 Camera not found. Please check your camera connection.")
            return
        
        st.info("🎥 Please look at the camera and press 'V' to capture your face.")
        play_audio_message("Please look at the camera and press V to capture your face")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("📸 Failed to capture image.")
                break

            # Add instructions overlay
            cv2.putText(frame, "Press 'V' to Capture | 'Q' to Quit", (20, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Sign Up - Face Capture", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
                
            if key == ord('v'):
                face_locations = face_recognition.face_locations(frame)
                if not face_locations:
                    st.warning("👤 No face detected. Please try again.")
                    play_audio_message("No face detected. Please try again")
                    continue
                    
                face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

                if is_face_registered(face_encoding):
                    st.error("⚠️ This face is already registered with another name.")
                    play_audio_message("This face is already registered with another name")
                    break

                try:
                    # Save user data
                    expiration_date = f"{expiration_month}/{expiration_year}"
                    user_data = {
                        "name": name,
                        "visa_number": visa_number,
                        "expiration_date": expiration_date,
                        "cvv": cvv,
                        "encoding": face_encoding.tolist()
                    }
                    
                    # Save JSON data
                    json_path = FACES_DIR / f"{name}.json"
                    with open(json_path, "w") as f:
                        json.dump(user_data, f)
                    
                    # Save face image
                    image_path = FACES_DIR / f"{name}.jpg"
                    cv2.imwrite(str(image_path), frame)
                    
                    success_msg = f"{name} has been registered successfully!"
                    st.success(f"✅ {success_msg}")
                    st.success(f"Data saved to {FACES_DIR}")
                    play_audio_message(success_msg)
                    
                except Exception as e:
                    st.error(f"Failed to save user data: {str(e)}")
                break

    except Exception as e:
        st.error(f"🚨 An error occurred during registration: {str(e)}")
    finally:
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()

########################################################################################

def main():
    st.title("📝 Register a New User")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px;'>
            <h3>🎯 Registration Process</h3>
            <ul>
                <li>Fill in your details</li>
                <li>Capture your face photo</li>
                <li>Verify your information</li>
                <li>Complete registration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Load and show animation
        lottie_animation = load_lottiefile(Login_Animation_file)
        st_lottie(lottie_animation, height=300)

    with col2:
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 1.5rem; border-radius: 10px;'>
            <h3>📋 Requirements</h3>
            <ul>
                <li>Full name (3 words min)</li>
                <li>Valid Visa card details</li>
                <li>Clear face photo</li>
                <li>Good lighting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📝 Registration Form")
    
    with st.container():
        st.markdown("""
        <div class='input-container'>
        """, unsafe_allow_html=True)
        
        # Camera selection
        available_cameras = [0, 1, 2, 3]
        camera_index = st.selectbox("📷 Select Camera", available_cameras, index=0,
                                  format_func=lambda x: f"Camera {x}")

        # Personal Information
        name = st.text_input("👤 Full Name (minimum 3 words)")
        
        # Payment Information
        visa_number = st.text_input("💳 Visa Number (16 digits)", type="password",max_chars=16)
        
        col1, col2 = st.columns(2)
        with col1:
            expiration_month = st.text_input("📅 Expiration Month (MM)",max_chars=2)
        with col2:
            expiration_year = st.text_input("📅 Expiration Year (YY)",max_chars=2)
            
        cvv = st.text_input("🔒 CVV (3 digits)", type="password",max_chars=3)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("✨ Register Now", key="register_button"):
            # Validate inputs
            if len(name.strip().split()) < 3:
                st.error("⚠️ Full name must be at least 3 words.")
            elif len(visa_number) != 16 or not visa_number.isdigit():
                st.error("⚠️ Invalid Visa number. Must be 16 digits.")
            elif not (len(expiration_month) == 2 and expiration_month.isdigit() and 1 <= int(expiration_month) <= 12):
                st.error("⚠️ Invalid month. Must be 2 digits between 01-12.")
            elif len(expiration_year) != 2 or not expiration_year.isdigit():
                st.error("⚠️ Invalid year. Must be 2 digits.")
            elif len(cvv) != 3 or not cvv.isdigit():
                st.error("⚠️ Invalid CVV. Must be 3 digits.")
            else:
                with st.spinner("📸 Starting registration process..."):
                    register_user(camera_index, name, visa_number, expiration_month, expiration_year, cvv)

if __name__ == "__main__":
    main()