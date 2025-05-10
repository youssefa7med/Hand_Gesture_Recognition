import streamlit as st
import cv2
import face_recognition
import os
import json
import numpy as np
from pathlib import Path
from streamlit_lottie import st_lottie
import time
import pyttsx3
from datetime import datetime
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
from ultralytics import YOLO
import cvzone

is_logged_in = False
logged_in_user = None

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
Login_Animation_file = current_dir.parent / "assets" / "Login_Animation.json"
model_path = str(current_dir.parent / "assets" / "best.pt")

st.markdown("""
    <style>
    .error-message {
        color: #ff4b4b;
        font-size: 18px;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #ff4b4b;
    }
    .warning-message {
        color: #ffa421;
        border-color: #ffa421;
    }
    .success-message {
        color: #00cc00;
        border-color: #00cc00;
    }
    </style>
""", unsafe_allow_html=True)

########################################################################################

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

########################################################################################

def load_registered_users():
    users = {}
    if os.path.exists("faces"):
        for file in os.listdir("faces"):
            if file.endswith(".json"):
                with open(os.path.join("faces", file), "r") as f:
                    user_data = json.load(f)
                    users[user_data['name']] = np.array(user_data['encoding'])
    return users

########################################################################################

def login_user(camera_index):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        return None, "camera_error"

    users = load_registered_users()
    model = YOLO(model_path)
    classNames = ["fake", "real"]
    confidence_threshold = 0.6

    while True:
        ret, frame = cap.read()
        if not ret:
            return None, "capture_error"

        frame = cv2.flip(frame, 1)
        cv2.putText(frame, "Press L to login & Press Q to quit", (180, 350),cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)
        cv2.imshow("Login - Face Capture", frame)


        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        if key == ord('l'):
            face_locations = face_recognition.face_locations(frame)
            if not face_locations:
                return None, "no_face"
            
            spoof_results = model(frame, stream=True, verbose=False)
            is_real = False
            for result in spoof_results:
                for box in result.boxes:
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    if conf > confidence_threshold and classNames[cls] == "real":
                        is_real = True
                        break
            
            if not is_real:
                return None, "spoofed"

            # التعرف على الوجه
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
            for name, encoding in users.items():
                if face_recognition.compare_faces([encoding], face_encoding)[0]:
                    cap.release()
                    cv2.destroyAllWindows()
                    return name, "success"

            return None, "not_registered"

    cap.release()
    cv2.destroyAllWindows()
    return None, "unknown_error"

########################################################################################

def start_anti_spoofing_verification(user_name):
    hand_detector = HandDetector(detectionCon=0.8, maxHands=1)
    face_detector = FaceDetector(minDetectionCon=0.7)
    model = YOLO(model_path)
    classNames = ["fake", "real"]

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    save_folder = "screenshots"
    os.makedirs(save_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    face_area = (100, 100, 200, 200)
    hand_area = (300, 100, 200, 200)

    start_time = None
    success_flag = False
    sound_played = False
    screenshot_taken = False
    greeting_played = False
    User_Name = user_name.split(" ")[0]
    confidence = 0.6
    countdown = 5

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        h, w, _ = img.shape

        if not greeting_played:
            engine.say(f"Hello {User_Name}, please place your face in the box and show an OK hand sign")
            engine.runAndWait()
            greeting_played = True

        img, faces = face_detector.findFaces(img, draw=False)
        face_inside = False
        face_real = False

        if faces and len(faces) == 1:
            face = faces[0]
            fx, fy = face["center"]
            if face_area[0] < fx < face_area[0] + face_area[2] and face_area[1] < fy < face_area[1] + face_area[3]:
                face_inside = True
                results = model(img, stream=True, verbose=False)
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        w, h = x2 - x1, y2 - y1
                        conf = float(box.conf[0])
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

        cv2.rectangle(img, (face_area[0], face_area[1]),
                        (face_area[0] + face_area[2], face_area[1] + face_area[3]),
                        (0, 255, 0) if face_inside else (0, 0, 255), 2)
        cv2.putText(img, "Place Face Here", (face_area[0], face_area[1] + face_area[3] + 20),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0) if face_inside else (0, 0, 255), 2)

        cv2.rectangle(img, (hand_area[0], hand_area[1]),
                        (hand_area[0] + hand_area[2], hand_area[1] + hand_area[3]),
                        (0, 255, 0) if hand_inside and ok_sign else (0, 0, 255), 2)
        cv2.putText(img, "Show OK Hand Sign", (hand_area[0], hand_area[1] + hand_area[3] + 20),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0) if hand_inside and ok_sign else (0, 0, 255), 2)

        if face_inside and face_real and hand_inside and ok_sign:
            if start_time is None:
                start_time = time.time()

            elapsed_time = time.time() - start_time
            countdown = max(0, 5 - int(elapsed_time))

            if countdown == 0 and not success_flag:
                engine.say("Verification successful. Welcome!")
                engine.runAndWait()
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(save_folder, f"{User_Name}_{now}.jpg")
                cv2.imwrite(screenshot_path, img)
                success_flag = True

        if not (face_inside and face_real and hand_inside and ok_sign):
            start_time = None
            countdown = 5
        cv2.putText(img, f"Hold steady: {countdown}s", (200, 400),
        cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 2)

        if success_flag:
            cv2.putText(img, "Press R to reset or Q to quit", (180, 450),cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)
        cv2.imshow("Verification", img)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            success_flag = False
            start_time = None
            countdown = 5
            engine.say("Resetting verification. Please start again.")
            engine.runAndWait()

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

########################################################################################

def main():
    global is_logged_in, logged_in_user

    st.markdown("""
    <style>
    .main-title {
        font-size: 2.8rem !important;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 25px;
    }
    .login-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background: #ffffff;
    }
    .camera-feed {
        border: 3px solid #3498db;
        border-radius: 10px;
        padding: 10px;
        margin: 20px 0;
    }
    .stButton>button {
        width: 100%;
        padding: 15px;
        border-radius: 8px;
        font-size: 1.1rem;
        background: #3498db;
        color: white;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: #2980b9;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<h1 class="main-title">🔒 Face Authentication System</h1>', unsafe_allow_html=True)
        
        col_anim, col_info = st.columns([2, 1])
        with col_anim:
            lottie_animation = load_lottiefile(str(Login_Animation_file))
            st_lottie(lottie_animation, height=200, key="login_anim")
        
        with col_info:
            st.markdown("""
            ### Secure Login Features:
            - 🚀 Instant face recognition
            - 🛡️ Anti-spoofing protection
            - 📸 Real-time verification
            """)

        st.divider()

        with st.container():
            st.markdown("### Ready to Authenticate?")
            if st.button("🚀 Start Face Verification", key="main_login"):
                with st.spinner("Initializing security protocols..."):
                    user_name, status = login_user(0)
                    if user_name:
                        with st.spinner("Performing deep verification..."):
                            start_anti_spoofing_verification(user_name)
                            st.balloons()
                            st.session_state.logged_in = True
                            st.success(f"✨ Welcome back, {user_name}!")
                    else:
                        self.handle_error(status)

        with st.expander("ℹ️ Need Help?", expanded=False):
            st.markdown("""
            **Common Issues Solution:**
            - 🧭 Position your face in center
            - 💡 Ensure good lighting
            - 📵 Avoid using photos/screens
            - 🔄 Restart system if needed
            """)

def handle_error(self, status):
    error_config = {
        "not_registered": {
            "icon": "🆔",
            "message": "Unregistered Identity Detected",
            "solution": "Please complete registration first"
        },
        "spoofed": {
            "icon": "🕵️",
            "message": "Spoofing Attempt Blocked!",
            "solution": "Use real face for authentication"
        },
        "no_face": {
            "icon": "👤",
            "message": "No Face Detected",
            "solution": "Adjust position and try again"
        },
        "camera_error": {
            "icon": "📷",
            "message": "Camera Connection Failed",
            "solution": "Check hardware connections"
        }
    }
    
    error_data = error_config.get(status, {
        "icon": "❌",
        "message": "Authentication Failed",
        "solution": "Unknown error occurred"
    })

    with st.container():
        st.markdown(f"""
        <div style="border-left: 4px solid #e74c3c; padding: 15px; background: #fdedec; border-radius: 5px; margin: 20px 0;">
            <h3>{error_data['icon']} {error_data['message']}</h3>
            <p>{error_data['solution']}</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()