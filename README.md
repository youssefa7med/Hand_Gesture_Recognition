# Hand Gesture Recognition

![GIF](https://www.bing.com/th/id/OGC.70ce94cc2a1ba1840824f847083eb506?pid=1.7&rurl=https%3a%2f%2fcdn.dribbble.com%2fusers%2f1637182%2fscreenshots%2f4904044%2fmedia%2f9521d26934e59e64c3f5efe711fb6f10.gif&ehk=EarpONZMtxg2YuTfqrCpvatq4xz1dy3R4MWbgzCKTGU%3d)

This project implements a **Hand Gesture Recognition** system capable of detecting and classifying hand gestures in real-time using computer vision and deep learning techniques.

## Overview

The system captures live video from the user's camera, processes the frames, detects hand regions, and classifies the hand gesture based on a trained model.

### Key Features

- **Hand Detection**:
  - Real-time hand tracking using MediaPipe Hands solution.
  
- **Gesture Classification**:
  - Classify hand gestures using a trained deep learning model.
  - Model trained on collected hand landmarks data.

- **User Interaction**:
  - Users can add new gesture classes easily.
  - Option to record new training data through the camera feed.

- **Real-time Prediction**:
  - Smooth and responsive prediction directly from webcam input.

## Technologies Used

- **Python**: Core language used.
- **OpenCV**: For camera handling and image processing.
- **Mediapipe**: For real-time hand tracking and landmark extraction.
- **Scikit-learn**: For training machine learning models.
- **Streamlit**: For creating an interactive web app to demonstrate gesture recognition.
- **NumPy & Pandas**: For data handling and manipulation.

## Project Structure

- `Collect_Data.py`: 
  - Script to collect and save landmarks data for custom hand gestures.
  
- `Model.py`: 
  - Model training script that uses collected landmarks to train a classifier.

- `App.py`: 
  - Main application file for real-time gesture recognition with Streamlit interface.

- `data/`: 
  - Folder to store captured hand landmarks CSV files.

- `model/`: 
  - Folder where trained models are saved.

## How to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/youssefa7med/Hand_Gesture_Recognition.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd Hand_Gesture_Recognition
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Collect Data (Optional)**:
   - Run to collect new gesture samples:
     ```bash
     python Collect_Data.py
     ```

5. **Train the Model**:
   - Train your model on collected data:
     ```bash
     python Model.py
     ```

6. **Run the Application**:
   - Launch the Streamlit app:
     ```bash
     streamlit run App.py
     ```

## Usage

- When the app starts, allow access to your camera.
- Perform one of the predefined gestures in front of the camera.
- The app will display the detected gesture in real-time.
- You can add new gestures by collecting new data and retraining the model.

## Future Improvements

- Enhance gesture classification accuracy using deep learning.
- Add support for multiple hands.
- Integrate gesture-based control for other applications (e.g., controlling slides or games).

## Contributing

Feel free to fork the project, open issues, and submit pull requests.  
Your contributions are highly welcome!

## License

This project is licensed under the MIT License.

---
🔗 [Project Repository](https://github.com/youssefa7med/Hand_Gesture_Recognition)
