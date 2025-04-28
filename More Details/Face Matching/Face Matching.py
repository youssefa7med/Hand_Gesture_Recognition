import cv2
import os
import json
import numpy as np
import face_recognition

FACES_DIR = "faces"

def register_face():
    name = input("Enter your name: ")
    visa_number = input("Enter your 16-digit Visa number: ")
    expiration_date = input("Enter expiration date (MM/YY): ")
    cvv = input("Enter 3-digit CVV: ")

    if len(visa_number) != 16 or not visa_number.isdigit():
        print("❌ Invalid Visa number.")
        return
    if len(cvv) != 3 or not cvv.isdigit():
        print("❌ Invalid CVV.")
        return
    if len(expiration_date.split("/")) != 2:
        print("❌ Invalid expiration date.")
        return

    cap = cv2.VideoCapture(0)
    print("📸 Please look at the camera... Press 'v' to capture your face.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture image.")
            break

        cv2.imshow("Face Registration", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("v"):  # Capture the photo when 'v' is pressed
            face_locations = face_recognition.face_locations(frame)
            if not face_locations:
                print("❌ No face detected.")
                continue

            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

            data = {
                "name": name,
                "visa_number": visa_number,
                "expiration_date": expiration_date,
                "cvv": cvv,
                "encoding": face_encoding.tolist()
            }

            if not os.path.exists(FACES_DIR):
                os.makedirs(FACES_DIR)

            with open(os.path.join(FACES_DIR, f"{name}.json"), "w") as f:
                json.dump(data, f)

            cv2.imwrite(os.path.join(FACES_DIR, f"{name}.jpg"), frame)

            print(f"✅ {name} has been registered successfully.")
            break

    cap.release()
    cv2.destroyAllWindows()

def load_faces():
    encodings = []
    names = []
    visas = {}

    if not os.path.exists(FACES_DIR):
        os.makedirs(FACES_DIR)
        print("⚠️ No registered data found.")
        return load_faces()

    json_files = [f for f in os.listdir(FACES_DIR) if f.endswith(".json")]
    if not json_files:
        print("⚠️ No registered data found.")
        return load_faces()

    for file in json_files:
        try:
            with open(os.path.join(FACES_DIR, file), "r") as f:
                data = json.load(f)
                if "encoding" not in data:
                    print(f"⚠️ Skipping {file} (no encoding found)")
                    continue
                encodings.append(np.array(data["encoding"]))
                names.append(data["name"])
                visas[data["name"]] = {
                    "visa_number": data["visa_number"],
                    "expiration_date": data["expiration_date"],
                    "cvv": data["cvv"]
                }
        except Exception as e:
            print(f"❌ Error loading {file}: {e}")

    if not encodings:
        print("⚠️ No valid data found.")
        return load_faces()

    return encodings, names, visas

def recognize_faces():
    known_encodings, known_names, visa_data = load_faces()
    cap = cv2.VideoCapture(0)

    print("🎥 Starting real-time face recognition. Press 'q' to quit, 'v' to capture a photo, or 'e' to register an unknown face.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture image.")
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None

            if best_match_index is not None and matches[best_match_index]:
                name = known_names[best_match_index]
                visa_number = visa_data[name]["visa_number"]
                masked_visa = "*" * 12 + visa_number[-4:]

                cv2.putText(frame, f"{name}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(frame, f"Visa: {masked_visa}", (left, bottom + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                print("❗ Unknown face detected.")
                cv2.putText(frame, "Press 'e' to register", (left, bottom + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0) if name != "Unknown" else (0, 0, 255), 2)

        cv2.imshow("Face Recognition", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("v"):  # Capture and save the image on pressing 'v'
            filename = "captured_face.jpg"
            cv2.imwrite(filename, frame)
            print(f"✅ Photo saved as {filename}")
        elif key == ord("e"):  # Register if 'e' is pressed
            register_face()  # Call the registration function

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()
