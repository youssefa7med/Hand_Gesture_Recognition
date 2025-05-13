import streamlit as st
from pathlib import Path
import json
from streamlit_lottie import st_lottie

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
Login_Animation_file = current_dir / "assets" / "Home_Animation.json"

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Custom CSS for enhanced UI
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .stat-card {
        background: linear-gradient(45deg, #4b6cb7, #182848);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .highlight {
        color: #4b6cb7;
        font-weight: 600;
    }
    .section-title {
        color: #2c3e50;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # st.set_page_config(page_title="Welcome | Face Recognition System", layout="wide")
    
    # Header Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("🌟 Welcome to Smart Face Recognition System")
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 1.5rem; border-radius: 10px;'>
        <h3>🎯 Your Gateway to Secure & Modern Authentication</h3>
        <p>Experience the future of security with our advanced face recognition system. 
        No more passwords to remember – your face is your key!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Load and display animation
        lottie_animation = load_lottiefile(Login_Animation_file)
        st_lottie(lottie_animation, height=200, key="home_anim")

    # System Statistics
    st.markdown("<h2 class='section-title'>📊 System Overview</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='stat-card'>
            <h2>99.9%</h2>
            <p>Recognition Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stat-card'>
            <h2>< 2s</h2>
            <p>Authentication Speed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stat-card'>
            <h2>+92%</h2>
            <p>Anti-Spoofing Rate</p>
        </div>
        """, unsafe_allow_html=True)

    # Core Features Section
    st.markdown("<h2 class='section-title'>🚀 Core Features</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>🔒 Advanced Security</h3>
            <ul>
                <li><b>AI-Powered Anti-Spoofing:</b> Detects and blocks photo/video attacks</li>
                <li><b>Real-time Liveness Detection:</b> Ensures authentic human presence</li>
                <li><b>Encrypted Data Storage:</b> Secure handling of biometric data</li>
                <li><b>Activity Monitoring:</b> Track and review authentication attempts</li>
            </ul>
        </div>
        
        <div class='feature-card'>
            <h3>👤 User Management</h3>
            <ul>
                <li><b>Quick Registration:</b> Simple 3-step signup process</li>
                <li><b>Profile Management:</b> Easy update of user information</li>
                <li><b>Multi-camera Support:</b> Use any connected camera</li>
                <li><b>Instant Verification:</b> < 2 second authentication time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>📊 Analytics Dashboard</h3>
            <ul>
                <li><b>User Statistics:</b> Track registration and usage patterns</li>
                <li><b>Security Logs:</b> Monitor authentication attempts</li>
                <li><b>Performance Metrics:</b> System health and response times</li>
                <li><b>Data Export:</b> Download reports in CSV format</li>
            </ul>
        </div>
        
        <div class='feature-card'>
            <h3>🎯 Smart Features</h3>
            <ul>
                <li><b>Voice Feedback:</b> Clear audio guidance during processes</li>
                <li><b>Adaptive Lighting:</b> Works in various lighting conditions</li>
                <li><b>Error Recovery:</b> Smart handling of failed attempts</li>
                <li><b>Modern UI:</b> Intuitive and responsive interface</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Getting Started Section
    st.markdown("<h2 class='section-title'>🌟 Getting Started</h2>", unsafe_allow_html=True)
    
    # Section 1: New User Registration
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; border: 1px solid #dee2e6;'>
            <h4 style='color: #4b6cb7; margin-bottom: 1rem; font-size: 1.2rem;'>1️⃣ New User Registration</h4>
            <div style='padding-left: 1rem;'>
                • Navigate to the <span style='color: #4b6cb7; font-weight: 600;'>Sign Up</span> page<br>
                • Enter your personal details<br>
                • Complete the face capture process<br>
                • Verify your information
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Section 2: Existing User Login
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; border: 1px solid #dee2e6;'>
            <h4 style='color: #4b6cb7; margin-bottom: 1rem; font-size: 1.2rem;'>2️⃣ Existing User Login</h4>
            <div style='padding-left: 1rem;'>
                • Go to the <span style='color: #4b6cb7; font-weight: 600;'>Login</span> page<br>
                • Position your face in the camera frame<br>
                • Wait for verification (usually < 2 seconds)<br>
                • Access granted upon successful verification
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Section 3: Managing Your Account
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; border: 1px solid #dee2e6;'>
            <h4 style='color: #4b6cb7; margin-bottom: 1rem; font-size: 1.2rem;'>3️⃣ Managing Your Account</h4>
            <div style='padding-left: 1rem;'>
                • Access the <span style='color: #4b6cb7; font-weight: 600;'>Dashboard</span> after login<br>
                • View your authentication history<br>
                • Update your profile information<br>
                • Monitor security logs
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
