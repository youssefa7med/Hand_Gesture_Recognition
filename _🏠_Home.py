import streamlit as st
from pathlib import Path
import json
from streamlit_lottie import st_lottie

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
Login_Animation_file = current_dir / "assets" / "Home_Animation.json"

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def main():
    st.set_page_config(page_title="Welcome | Face Recognition System", layout="centered")
    st.title("👋 Welcome to the Face Recognition System")

    # Load animation
    lottie_animation = load_lottiefile(Login_Animation_file)
    st_lottie(lottie_animation, height=250, key="home_anim")

    st.markdown("---")

    st.markdown("""
    ## 🔐 What is this system about?

    This is a **secure face recognition-based authentication system** that allows users to **sign up** and **log in** using only their face — no passwords required!

    ### ✨ Key Features:
    - **AI-Powered Anti-Spoofing**: Detects whether the face is real or fake.
    - **Real-Time Face Recognition**: Login in seconds with your camera.
    - **Fast & User-Friendly Interface**: Built using cutting-edge technologies.
    - **Secure Data Storage**: Your face data is stored securely and encrypted.

    ### 👨‍💻 Ideal Use Cases:
    - Secure access to sensitive platforms
    - Attendance systems for schools or companies
    - Smart home entry systems

    ---
    ### 🚀 Ready to get started?

    - Go to **Sign-Up** to register your face and details.
    - Already registered? Head to **Login** to access the system securely.
    """)

if __name__ == "__main__":
    main()
