import cv2
import mediapipe as mp
import math

# Initialize mediapipe hands and drawing utils
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Start the webcam
cap = cv2.VideoCapture(0)

# Function to check if a finger is open
def is_finger_open(hand_landmarks, finger_tip, finger_base):
    # Calculate the distance between the tip and base of the finger
    tip_x, tip_y = hand_landmarks[finger_tip].x, hand_landmarks[finger_tip].y
    base_x, base_y = hand_landmarks[finger_base].x, hand_landmarks[finger_base].y
    distance = math.sqrt((tip_x - base_x) ** 2 + (tip_y - base_y) ** 2)
    return distance > 0.05  # A threshold to determine if the finger is open

# Use the Mediapipe Hands model
with mp_hands.Hands(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Convert the image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Process the image and detect hands
        results = hands.process(image)

        # Convert the image back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # If hands are detected, draw landmarks
        if results.multi_hand_landmarks:
            print("Hand(s) detected")
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Count the number of fingers open
                open_fingers = 0
                for i in [4, 8, 12, 16, 20]:  # Checking tips of the fingers
                    if is_finger_open(hand_landmarks.landmark, i, i-2):
                        open_fingers += 1

                # Display the number of open fingers
                cv2.putText(image, f"Open Fingers: {open_fingers}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
        else:
            print("No hands detected")

        # Display the image
        cv2.imshow("Hand Tracking", image)

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and stop
cap.release()
cv2.destroyAllWindows()