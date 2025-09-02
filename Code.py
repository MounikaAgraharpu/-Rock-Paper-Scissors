import cv2
import mediapipe as mp
import random
import time
import pyttsx3 

# === Initialize Text-to-Speech ===
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Speaking rate

def speak(text):
    print(f" {text}")
    engine.say(text)
    engine.runAndWait()

# ===  Load Bot Images ===
rock_path = r"D:\Research\Promotion\4\Rock.JPG"
paper_path = r"D:\Research\Promotion\4\Paper.JPG"
scissors_path = r"D:\Research\Promotion\4\Scissors.JPG"

bot_images = {
    'rock': cv2.imread(rock_path),
    'paper': cv2.imread(paper_path),
    'scissors': cv2.imread(scissors_path)
}

for key, img in bot_images.items():
    if img is None:
        print(f" ERROR: Could not load image for {key}. Check path.")
    else:
        print(f" Loaded {key} image.")

# === MediaPipe Hands ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# ===  Game ===
moves = ['rock', 'paper', 'scissors']
player_score = 0
bot_score = 0
max_score = 5

tip_ids = [4, 8, 12, 16, 20]

def decide_winner(player, bot):
    if player == bot:
        return 'draw'
    elif (player == 'rock' and bot == 'scissors') or \
         (player == 'scissors' and bot == 'paper') or \
         (player == 'paper' and bot == 'rock'):
        return 'player'
    else:
        return 'bot'

def get_hand_gesture(results):
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        fingers = []

        if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = fingers.count(1)

        if total_fingers == 0:
            return 'rock'
        elif total_fingers == 2:
            return 'scissors'
        elif total_fingers >= 4:
            return 'paper'
    return None

# ===  Webcam & Timer ===
cap = cv2.VideoCapture(0)
print(" Show your hand: Rock (fist), Paper (open palm), Scissors (2 fingers)")
print(" Press 'q' to quit.")
speak("Let's play Rock Paper Scissors! First to five wins.")

last_move_time = 0
cooldown = 5  # seconds

while cap.isOpened() and player_score < max_score and bot_score < max_score:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    now = time.time()

    if results.multi_hand_landmarks:
        for lm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)

    cv2.putText(frame, f"You: {player_score}  Bot: {bot_score}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    time_left = max(0, int(last_move_time + cooldown - now))
    cv2.putText(frame, f"Next move in: {time_left}s", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    if now - last_move_time >= cooldown:
        gesture = get_hand_gesture(results)
        if gesture:
            bot_move = random.choice(moves)
            result = decide_winner(gesture, bot_move)

            if result == 'draw':
                text = f"Draw! Both chose {gesture}."
                speak(f"It's a draw! Both chose {gesture}.")
            elif result == 'player':
                player_score += 1
                text = f"You win! {gesture} beats {bot_move}."
                speak(f"You win! {gesture} beats {bot_move}.")
            else:
                bot_score += 1
                text = f"I won! {bot_move} beats {gesture}."
                speak(f"I won! {bot_move} beats {gesture}.")

            print(text)
            print(f"Score: You {player_score} - Bot {bot_score}")

            bot_img = bot_images[bot_move]
            if bot_img is not None:
                cv2.imshow("My Move", bot_img)
                cv2.waitKey(1000)
                cv2.destroyWindow("My Move")

            last_move_time = now

    cv2.imshow("Rock Paper Scissors - Webcam", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# ===  Final Voice Winner ===
if player_score > bot_score:
    final = "Congratulations! You won the game!"
else:
    final = "I won the game. Better luck next time!"

print(final)
speak(final)

cap.release()
cv2.destroyAllWindows()
