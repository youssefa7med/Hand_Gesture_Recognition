import streamlit as st
import cv2
import face_recognition
import os
import json
import numpy as np
from pathlib import Path
from streamlit_lottie import st_lottie

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
Login_Animation_file = current_dir.parent / "assets" / "Sign_up_Animation.json"
FACES_DIR = "faces"

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


########################################################################################


def load_registered_users():
    # Load all the registered user data (encodings)
    users = {}
    if os.path.exists(FACES_DIR):
        for file in os.listdir(FACES_DIR):
            if file.endswith(".json"):
                with open(os.path.join(FACES_DIR, file), "r") as f:
                    user_data = json.load(f)
                    users[user_data['name']] = np.array(user_data['encoding'])
    return users


########################################################################################


def is_face_registered(face_encoding):
    # Check if the face is already registered by comparing encodings
    registered_users = load_registered_users()
    for user, encoding in registered_users.items():
        matches = face_recognition.compare_faces([encoding], face_encoding)
        if any(matches):
            return True
    return False


########################################################################################


def register_user(camera_index, name, visa_number, expiration_month, expiration_year, cvv):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        st.error("Camera not found. Please check your camera connection.")
        return
    st.info("Please look at the camera and press 'v' to capture your face.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image.")
            break

        cv2.imshow("Sign Up - Face Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('v'):
            face_locations = face_recognition.face_locations(frame)
            if not face_locations:
                st.warning("No face detected. Try again.")
                continue
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

            # Check if face is already registered
            if is_face_registered(face_encoding):
                st.error("⚠️ This face is already registered with another name.")
                break

            expiration_date = f"{expiration_month}/{expiration_year}"
            user_data = {
                "name": name,
                "visa_number": visa_number,
                "expiration_date": expiration_date,
                "cvv": cvv,
                "encoding": face_encoding.tolist()
            }
            if not os.path.exists(FACES_DIR):
                os.makedirs(FACES_DIR)
            with open(os.path.join(FACES_DIR, f"{name}.json"), "w") as f:
                json.dump(user_data, f)
            cv2.imwrite(os.path.join(FACES_DIR, f"{name}.jpg"), frame)
            st.success(f"{name} has been registered successfully.")
            break
    cap.release()
    cv2.destroyAllWindows()


########################################################################################


def main():
    st.set_page_config(page_title="Sign Up", layout="centered")
    st.title("📝 Register a New User")

    lottie_animation = load_lottiefile(Login_Animation_file)
    st_lottie(lottie_animation, height=200)

    # Hardcoded list of available cameras (or can be dynamically generated if needed)
    available_cameras = [0, 1, 2, 3]  # Example camera indexes, modify based on your setup

    # Selectbox for the user to select a camera
    camera_index = st.selectbox("Select Camera", available_cameras, index=0)

    name = st.text_input("Please enter your full name.")
    visa_number = st.text_input("Visa Number (16 digits)", type="password")
    col1, col2 = st.columns(2)
    with col1:
        expiration_month = st.text_input("Expiration Month (MM)")
    with col2:
        expiration_year = st.text_input("Expiration Year (YY)")
    cvv = st.text_input("CVV (3 digits)", type="password")

    if st.button("Register"):
        if len(name.strip().split()) < 3:
            st.error("⚠️ Full name must be at least 3 words.")
        elif len(visa_number) != 16 or not visa_number.isdigit():
            st.error("⚠️ Invalid Visa number. Must be 16 digits.")
        elif len(expiration_month) != 2 or not expiration_month.isdigit():
            st.error("⚠️ Invalid month. Must be 2 digits.")
        elif len(expiration_year) != 2 or not expiration_year.isdigit():
            st.error("⚠️ Invalid year. Must be 2 digits.")
        elif len(cvv) != 3 or not cvv.isdigit():
            st.error("⚠️ Invalid CVV. Must be 3 digits.")
        else:
            register_user(camera_index, name, visa_number, expiration_month, expiration_year, cvv)

if __name__ == "__main__":
    main()
