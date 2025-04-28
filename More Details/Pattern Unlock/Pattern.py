import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

pattern = []
visited = set()
recording = False

box_size = 300
screen_w, screen_h = 640, 480
start_x = (screen_w - box_size) // 2
start_y = (screen_h - box_size) // 2

def get_cell(x, y):
    if x < start_x or x > start_x + box_size or y < start_y or y > start_y + box_size:
        return None
    col = (x - start_x) // (box_size // 3)
    row = (y - start_y) // (box_size // 3)
    return int(row * 3 + col + 1), int(row), int(col)

def distance(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def draw_grid(frame):
    for i in range(4):
        y = start_y + i * box_size // 3
        cv2.line(frame, (start_x, y), (start_x + box_size, y), (200, 200, 200), 2)
        x = start_x + i * box_size // 3
        cv2.line(frame, (x, start_y), (x, start_y + box_size), (200, 200, 200), 2)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (screen_w, screen_h))
    frame = cv2.flip(frame, 1)

    draw_grid(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            index_tip = (int(lm[8].x * screen_w), int(lm[8].y * screen_h))
            thumb_tip = (int(lm[4].x * screen_w), int(lm[4].y * screen_h))

            dist = distance(index_tip, thumb_tip)

            if dist < 40:
                recording = True
                center_x, center_y = index_tip

                cell_info = get_cell(center_x, center_y)
                if cell_info:
                    cell_num, row, col = cell_info
                    if cell_num not in visited:
                        visited.add(cell_num)
                        pattern.append(((row, col), (center_x, center_y)))
                        print("Selected:", cell_num)
            else:
                if recording:
                    print("Final Pattern:", [r*3 + c + 1 for (r, c), _ in pattern])
                recording = False

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    for i, ((row, col), center) in enumerate(pattern):
        cell_center = (
            int(start_x + (col + 0.5) * (box_size // 3)),
            int(start_y + (row + 0.5) * (box_size // 3))
        )
        cv2.circle(frame, cell_center, 15, (0, 255, 0), -1)
        if i > 0:
            prev_center = (
                int(start_x + (pattern[i - 1][0][1] + 0.5) * (box_size // 3)),
                int(start_y + (pattern[i - 1][0][0] + 0.5) * (box_size // 3))
            )
            cv2.line(frame, prev_center, cell_center, (0, 255, 255), 4)

    cv2.rectangle(frame, (start_x, start_y), (start_x + box_size, start_y + box_size), (255, 255, 255), 2)
    cv2.imshow("Pattern Unlock", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Final Pattern:", [r*3 + c + 1 for (r, c), _ in pattern])
        break

cap.release()
cv2.destroyAllWindows()
