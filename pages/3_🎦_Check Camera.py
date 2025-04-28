import streamlit as st
import cv2
import face_recognition
import numpy as np
import json
import os
import time
from PIL import Image
from streamlit_lottie import st_lottie
import json as js
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
Camera_Animation_file = current_dir.parent / "assets" / "Camera_Animation.json"
FACES_DIR = "faces"


########################################################################################


def list_available_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr


########################################################################################


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return js.load(f)


########################################################################################


def camera_selection_page():
    st.title("🎥 Select Your Camera")
    st.write("Choose a camera from the available list below:")

    lottie_animation = load_lottiefile(Camera_Animation_file)
    st_lottie(lottie_animation, height=200)

    available_cameras = list_available_cameras()

    if not available_cameras:
        st.error("No cameras found. Please connect a camera and try again.")
        return None

    camera_index = st.selectbox("Available Cameras", available_cameras)
    if st.button("Test Camera"):
        cap = cv2.VideoCapture(camera_index)
        st.info("Press 'q' to close the test window.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow(f"Testing Camera {camera_index}", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        st.success(f"Camera {camera_index} tested successfully!")

if __name__ == "__main__":
    camera_selection_page()