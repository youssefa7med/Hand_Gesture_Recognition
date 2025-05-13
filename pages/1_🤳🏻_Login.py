import streamlit as st
import cv2
import face_recognition
import os
import json
import numpy as np
from pathlib import Path
from streamlit_lottie import st_lottie
import time
from datetime import datetime
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
from ultralytics import YOLO
import cvzone
from gtts import gTTS
from io import BytesIO
import pygame
import math

# Initialize pygame mixer for audio
pygame.mixer.init()

# Create necessary directories
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
root_dir = current_dir.parent
FACES_DIR = root_dir / "faces"
SCREENSHOTS_DIR = root_dir / "screenshots"

# Ensure directories exist
FACES_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

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

st.set_page_config(page_title="Face Login System", layout="wide")

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
    .stSelectbox {
        border-radius: 10px;
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 2rem;
    }
    .camera-container {
        border: 2px solid #4b6cb7;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

is_logged_in = False
logged_in_user = None

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
Login_Animation_file = current_dir.parent / "assets" / "Login_Animation.json"
model_path = str(current_dir.parent / "assets" / "best.pt")

########################################################################################

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

########################################################################################

def load_registered_users():
    users = {}
    try:
        if FACES_DIR.exists():
            for file in FACES_DIR.glob("*.json"):
                with open(file, "r") as f:
                    user_data = json.load(f)
                    users[user_data['name']] = np.array(user_data['encoding'])
    except Exception as e:
        st.error(f"Error loading registered users: {str(e)}")
    return users

########################################################################################

def login_user(camera_index):
    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            st.error("📷 Camera not found. Please check your camera connection.")
            return None

        st.info("🎥 Please face the camera and press 'L' to start recognition or 'Q' to quit.")
        play_audio_message("Please face the camera and press L to start recognition")

        users = load_registered_users()
        if not users:
            st.warning("⚠️ No registered users found. Please register first.")
            return None

        model = YOLO(model_path)
        classNames = ["fake", "real"]
        confidence_threshold = 0.6

        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("📸 Failed to capture image.")
                break

            # Add instructions overlay
            cv2.putText(frame, "Press 'L' to Login | 'Q' to Quit", (20, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Login - Face Capture", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

            if key == ord('l'):
                face_locations = face_recognition.face_locations(frame)
                if not face_locations:
                    st.warning("👤 No face detected. Please try again.")
                    play_audio_message("No face detected. Please try again")
                    continue

                face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

                spoof_results = model(frame, stream=True, verbose=False)
                is_real = False

                for result in spoof_results:
                    for box in result.boxes:
                        conf = float(box.conf[0])
                        cls = int(box.cls[0])
                        label = classNames[cls]
                        if conf > confidence_threshold and label == "real":
                            is_real = True
                            break

                if not is_real:
                    st.error("🚫 Spoof detected! Please use your real face.")
                    play_audio_message("Spoof detected! Please use your real face")
                    continue

                for name, encoding in users.items():
                    matches = face_recognition.compare_faces([encoding], face_encoding)
                    if any(matches):
                        welcome_msg = f"Welcome back, {name.split(' ')[0]}!"
                        st.success(f"✨ {welcome_msg}")
                        play_audio_message(welcome_msg)
                        cap.release()
                        cv2.destroyAllWindows()
                        return name

                st.error("❌ Face not recognized. Please register first.")
                play_audio_message("Face not recognized. Please register first")
                continue

    except Exception as e:
        st.error(f"🚨 An error occurred: {str(e)}")
        return None
    finally:
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()

    return None

########################################################################################

def start_anti_spoofing_verification(user_name):
    try:
        hand_detector = HandDetector(detectionCon=0.8, maxHands=1)
        face_detector = FaceDetector(minDetectionCon=0.7)
        model = YOLO(model_path)
        classNames = ["fake", "real"]

        # Ensure screenshots directory exists
        SCREENSHOTS_DIR.mkdir(exist_ok=True)

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        # Detection zones
        face_area = (100, 100, 200, 200)
        hand_area = (300, 100, 200, 200)

        # Flags and timers
        start_time = None
        success_flag = False
        sound_played = False
        screenshot_taken = False
        greeting_played = False
        User_Name = user_name.split(" ")[0]
        confidence = 0.6

        # FPS tracking
        prev_frame_time = 0
        new_frame_time = 0

        # Initial greeting
        greeting_msg = f"Hello {User_Name}, please place your face in the box and show an OK hand sign"
        play_audio_message(greeting_msg)
        greeting_played = True

        while True:
            new_frame_time = time.time()
            success, img = cap.read()
            if not success:
                st.error("Failed to capture frame from camera")
                break
                
            img = cv2.flip(img, 1)
            h, w, _ = img.shape

            img, faces = face_detector.findFaces(img, draw=True)
            face_inside = False
            face_real = False

            if faces and len(faces) == 1:
                face = faces[0]
                fx, fy = face["center"]
                if face_area[0] < fx < face_area[0] + face_area[2] and face_area[1] < fy < face_area[1] + face_area[3]:
                    face_inside = True

                    # Run YOLO detection
                    results = model(img, stream=True, verbose=False)
                    for r in results:
                        boxes = r.boxes
                        for box in boxes:
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            w, h = x2 - x1, y2 - y1
                            conf = math.ceil((box.conf[0] * 100)) / 100
                            cls = int(box.cls[0])

                            if conf > confidence:
                                label = classNames[cls]
                                color = (0, 255, 0) if label == "real" else (0, 0, 255)
                                cvzone.cornerRect(img, (x1, y1, w, h), colorC=color, colorR=color)
                                cvzone.putTextRect(img, f'{label.upper()} {int(conf*100)}%',
                                                (max(0, x1), max(35, y1)), scale=2, thickness=4,
                                                colorR=color, colorB=color)
                                if label == 'real':
                                    face_real = True

            hands, img = hand_detector.findHands(img, flipType=False)
            hand_inside = False
            ok_sign = False

            if hands:
                hand = hands[0]
                lmList = hand["lmList"]
                cx, cy = hand["center"]
                if hand_area[0] < cx < hand_area[0] + hand_area[2] and hand_area[1] < cy < hand_area[1] + hand_area[3]:
                    hand_inside = True

                thumb_tip = lmList[4][:2]
                index_tip = lmList[8][:2]
                dist = ((thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2) ** 0.5
                if dist < 40:
                    ok_sign = True

            # Show detection zone boxes with modern style
            cvzone.cornerRect(img, (face_area[0], face_area[1], face_area[2], face_area[3]),
                            colorC=(0, 255, 0) if face_inside else (0, 0, 255),
                            colorR=(0, 255, 0) if face_inside else (0, 0, 255))
            cvzone.putTextRect(img, "Place Face Here", 
                             (face_area[0], face_area[1] - 10),
                             scale=2, thickness=2,
                             colorR=(0, 255, 0) if face_inside else (0, 0, 255))

            cvzone.cornerRect(img, (hand_area[0], hand_area[1], hand_area[2], hand_area[3]),
                            colorC=(0, 255, 0) if hand_inside and ok_sign else (0, 0, 255),
                            colorR=(0, 255, 0) if hand_inside and ok_sign else (0, 0, 255))
            cvzone.putTextRect(img, "Show OK Hand Sign",
                             (hand_area[0], hand_area[1] - 10),
                             scale=2, thickness=2,
                             colorR=(0, 255, 0) if hand_inside and ok_sign else (0, 0, 255))

            if face_inside and face_real and hand_inside and ok_sign and not success_flag:
                if start_time is None:
                    start_time = time.time()

                elapsed = time.time() - start_time
                remaining = int(5 - elapsed)
                
                if remaining > 0:
                    cvzone.putTextRect(img, f"Hold steady: {remaining}s", (200, 400),
                                     scale=2, thickness=3, colorR=(0, 255, 0))
                elif not success_flag:
                    success_flag = True
            else:
                if not success_flag:
                    start_time = None

            if success_flag:
                if not screenshot_taken:
                    try:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        screenshot_path = SCREENSHOTS_DIR / f"{User_Name}_screenshot_{timestamp}.png"
                        cv2.imwrite(str(screenshot_path), img)
                        screenshot_taken = True
                        st.success(f"Screenshot saved to {screenshot_path}")
                    except Exception as e:
                        st.error(f"Failed to save screenshot: {str(e)}")

                if not sound_played:
                    play_audio_message("Thank you for verifying your identity")
                    sound_played = True

                cvzone.putTextRect(img, "Press R to reset or Q to quit", (180, 450),
                                 scale=1.5, thickness=2)

            # Calculate and display FPS
            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            cvzone.putTextRect(img, f"FPS: {int(fps)}", (20, 40),
                             scale=1.5, thickness=2)

            cv2.imshow("Verification", img)

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('r'):
                start_time = None
                success_flag = False
                sound_played = False
                screenshot_taken = False
                greeting_played = True
                play_audio_message("Resetting verification. Please start again.")

    except Exception as e:
        st.error(f"🚨 An error occurred during verification: {str(e)}")
    finally:
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()

########################################################################################

def main():
    global is_logged_in, logged_in_user

    st.title("🔐 Face Recognition Login Portal")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px;'>
            <h3>🚀 Secure Login Features</h3>
            <ul>
                <li>Advanced Face Recognition</li>
                <li>Anti-spoofing Protection</li>
                <li>Hand Gesture Verification</li>
                <li>Real-time Processing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Load and show animation
        lottie_animation = load_lottiefile(str(Login_Animation_file))
        st_lottie(lottie_animation, height=300, key="login_anim")

    with col2:
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 1.5rem; border-radius: 10px;'>
            <h3>📋 Instructions</h3>
            <ol>
                <li>Select your camera</li>
                <li>Click Login button</li>
                <li>Press 'L' to capture</li>
                <li>Follow the prompts</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📷 Camera Selection")
        cameras = [0, 1, 2, 3]
        camera_index = st.selectbox("Choose your camera", cameras, index=0,
                                  format_func=lambda x: f"Camera {x}")

        if st.button("🔓 Login", key="login_button"):
            with st.spinner("🎥 Initializing face recognition..."):
                user_name = login_user(camera_index)
                if user_name:
                    with st.spinner("🔍 Running security verification..."):
                        start_anti_spoofing_verification(user_name)
                        is_logged_in = True
                        logged_in_user = user_name
                        st.success(f"✅ Welcome, {user_name}! Login successful!")
                        st.balloons()

if __name__ == "__main__":
    main()