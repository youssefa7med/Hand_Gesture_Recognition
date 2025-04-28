import cv2
import time
import pyttsx3
from datetime import datetime
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector

hand_detector = HandDetector(detectionCon=0.8, maxHands=1)
face_detector = FaceDetector(minDetectionCon=0.7)
engine = pyttsx3.init()
engine.setProperty('rate', 150)

cap = cv2.VideoCapture(0)

face_area = (100, 100, 200, 200)
hand_area = (300, 100, 200, 200)

start_time = None
success_flag = False
sound_played = False
screenshot_taken = False
greeting_played = False
User_Name = "Youssef"

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    if not greeting_played:
        engine.say(f"Hello {User_Name}, please place your face in the box and show an OK hand sign")
        engine.runAndWait()
        greeting_played = True

    img, faces = face_detector.findFaces(img, draw=True)
    face_inside = False
    if faces and len(faces) == 1:
        face = faces[0]
        fx, fy = face["center"]
        if face_area[0] < fx < face_area[0] + face_area[2] and face_area[1] < fy < face_area[1] + face_area[3]:
            face_inside = True

    hands, img = hand_detector.findHands(img, flipType=False)
    hand_inside = False
    ok_sign = False

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        cx, cy = hand["center"]

        if hand_area[0] < cx < hand_area[0] + hand_area[2] and hand_area[1] < cy < hand_area[1] + hand_area[3]:
            hand_inside = True

        # OK sign check (thumb tip - index tip)
        thumb_tip = lmList[4][:2]
        index_tip = lmList[8][:2]
        dist = ((thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2) ** 0.5
        if dist < 40:
            ok_sign = True

    cv2.rectangle(img, (face_area[0], face_area[1]),
                    (face_area[0] + face_area[2], face_area[1] + face_area[3]),
                    (0, 255, 0) if face_inside else (0, 0, 255), 2)
    cv2.putText(img, "Place Face Here", (face_area[0], face_area[1] - 10),
                cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0) if face_inside else (0, 0, 255), 2)

    cv2.rectangle(img, (hand_area[0], hand_area[1]),
                    (hand_area[0] + hand_area[2], hand_area[1] + hand_area[3]),
                    (0, 255, 0) if hand_inside and ok_sign else (0, 0, 255), 2)
    cv2.putText(img, "Show OK Hand Sign", (hand_area[0], hand_area[1] - 10),
                cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0) if hand_inside and ok_sign else (0, 0, 255), 2)

    if face_inside and hand_inside and ok_sign and not success_flag:
        if start_time is None:
            start_time = time.time()

        elapsed = time.time() - start_time
        remaining = int(5 - elapsed)
        if remaining > 0:
            cv2.putText(img, f"Hold steady: {remaining}s", (200, 400),
                        cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 2)
        elif not success_flag:
            success_flag = True
    else:
        if not success_flag:
            start_time = None

    if success_flag:
        if not screenshot_taken:
            # Save screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f"screenshot_{timestamp}.png", img)
            screenshot_taken = True

        if not sound_played:
            engine.say("Thank you for verifying your identity")
            engine.runAndWait()
            sound_played = True

        cv2.putText(img, "Press R to reset or Q to quit", (180, 450),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)

    cv2.imshow("Verification", img)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('r'):
        # Reset everything
        start_time = None
        success_flag = False
        sound_played = False
        screenshot_taken = False
        greeting_played = True

cap.release()
cv2.destroyAllWindows()
