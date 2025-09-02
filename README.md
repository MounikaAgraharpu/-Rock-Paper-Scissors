## Rock Paper Scissors - Real-Time Webcam Game with Voice Over
## 🎬 Demo Video

Click below to watch the demo video of this project in action:

[![Watch the Demo](docs/demo_thumb.png)](https://drive.google.com/file/d/1kXBHt9IgHR43Ro8Ia8znH6oqdBPagc3T/view?usp=sharing)


A fun Python project: play Rock Paper Scissors against a bot using your webcam — with voice announcements!

---

## How it works

- Uses your webcam + [MediaPipe](https://google.github.io/mediapipe/) to detect your hand.
- Recognizes:
  - ✊ Fist → Rock
  - ✋ Open palm → Paper
  - ✌️ Two fingers → Scissors
- Bot picks randomly.
- Text-to-speech announces each round’s result.
- First to 5 points wins!

---

## Setup

Clone this repo  
```bash
git clone https://github.com/YOUR_USERNAME/rock-paper-scissors-bot.git
cd rock-paper-scissors-bot

## Install dependencies
pip install -r requirements.txt

##Make sure your bot_images/ folder contains:
![Bot Rock](https://drive.google.com/uc?id=1bp743KdCm1n1mdtsD18q4-W6xdhUt6EU)

![Bot Paper](https://drive.google.com/file/d/1biB5I-xFXb_-JS295uSv5laCdVAhL3oQ/view?usp=sharing)

![Bot Scissors](docs/demo.png)(https://drive.google.com/file/d/1pjbCsOtXKNilHtVBlz38N78JnlQE5q0a/view?usp=sharing)

## python Code.py



