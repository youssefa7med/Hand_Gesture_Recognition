# 🌟 Smart Face Recognition System

A modern, AI-powered face recognition system with anti-spoofing capabilities, built using cutting-edge technologies for secure and efficient authentication.

![System Demo](https://www.bing.com/th/id/OGC.70ce94cc2a1ba1840824f847083eb506?pid=1.7&rurl=https%3a%2f%2fcdn.dribbble.com%2fusers%2f1637182%2fscreenshots%2f4904044%2fmedia%2f9521d26934e59e64c3f5efe711fb6f10.gif&ehk=EarpONZMtxg2YuTfqrCpvatq4xz1dy3R4MWbgzCKTGU%3d)

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Features

### 🔒 Security
- **Advanced Face Recognition**: High-accuracy facial feature extraction and matching
- **Anti-Spoofing Protection**: AI-powered liveness detection using YOLOv5
- **Secure Data Storage**: Encrypted storage of facial features and user data
- **Activity Monitoring**: Comprehensive logging of all authentication attempts

### 👤 User Experience
- **Modern UI**: Clean, responsive interface built with Streamlit
- **Voice Feedback**: Clear audio guidance using gTTS
- **Multi-Camera Support**: Compatible with various camera inputs
- **Quick Registration**: Streamlined 3-step signup process

### 📊 Analytics
- **User Dashboard**: Track registration and authentication patterns
- **Performance Metrics**: Monitor system health and response times
- **Export Capabilities**: Download user data and authentication logs
- **Visual Analytics**: Interactive charts and statistics

## 🛠️ Technology Stack

### Core Components
```python
face_recognition==1.3.0    # Face detection and encoding
opencv-python==4.8.0       # Image processing and camera handling
ultralytics==8.0.0         # YOLOv5 for anti-spoofing
```

### UI & Interaction
```python
streamlit==1.28.0          # Web interface
gtts==2.3.2               # Text-to-speech feedback
pygame==2.5.0             # Audio playback
```

### Data Management
```python
numpy==1.24.0             # Numerical operations
pandas==2.0.0             # Data manipulation
plotly==5.13.0            # Interactive visualizations
```

## 📁 Project Structure

```
project/
├── 🏠_Home.py                # Main application entry
├── pages/
│   ├── 1_🤳🏻_Login.py        # Login interface
│   ├── 2_✍🏻_Sign Up.py       # User registration
│   └── 3_📊_Dashboard.py      # Analytics dashboard
├── assets/
│   ├── best.pt              # YOLOv5 model
│   └── animations/          # UI animations
├── faces/                   # User face data
├── screenshots/             # Verification attempts
└── requirements.txt         # Dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Webcam or USB camera
- Windows/Linux/MacOS

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/face-recognition-system.git
cd face-recognition-system
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
streamlit run 🏠_Home.py
```

## 💡 Usage Guide

### 1. Registration Process
1. Navigate to "Sign Up" page
2. Enter personal details
3. Complete face capture
4. Verify information

### 2. Login Process
1. Go to "Login" page
2. Position face in camera frame
3. Wait for verification
4. Access granted upon success

### 3. Dashboard Features
1. View user statistics
2. Monitor authentication history
3. Export data reports
4. Update user information

## 🔧 Configuration

Key configuration options are available in the respective page files:

- Camera selection
- Face detection sensitivity
- Anti-spoofing confidence threshold
- Authentication timeout

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
```bash
git checkout -b feature/AmazingFeature
```
3. Commit your changes
```bash
git commit -m 'Add some AmazingFeature'
```
4. Push to the branch
```bash
git push origin feature/AmazingFeature
```
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- Face recognition library
- YOLOv8 by Ultralytics
- Streamlit team for the amazing framework
- OpenCV community for computer vision tools



