# ♛ CGACChess - Ultimate Chess Client

![Version](https://img.shields.io/badge/version-0.3.0-blue)
![Python](https://img.shields.io/badge/python-3.13-yellow)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

A modern, feature-rich chess experience built with Python, PyQt5, and python-chess.  
**Made with ❤️ by a team of two Iranian developers (average age: 14.5).**

---

## 🎮 Download

**Available now on itch.io:**  
👉 [**Download CGACChess on itch.io**](https://mkiya.itch.io/cgacchess)

---

## ✨ Features

### ♟️ Gameplay
- **Play vs AI** — 3 difficulty levels (Easy, Medium, Hard) with Stockfish engine support
- **Local 2-Player Mode** — Play with a friend on the same device
- **LAN Multiplayer** — Connect and play with friends over local network (TCP sockets)
- **Custom Time Controls** — 3, 5, and 10-minute modes

### 🧠 Learning & Practice
- **Daily Challenge** — A new tactical puzzle every day
- **Interactive Lessons** — Learn chess rules (pawns, knights, castling, en passant, etc.)
- **Practice Mode** — Solve puzzles by category (Fork, Pin, Skewer, Mate in 1/2)
- **Openings Library** — 20+ classic openings (Italian, Sicilian, Ruy Lopez, Queen's Gambit...)
- **Endgames Trainer** — K+P vs K, K+R vs K, Lucena position, and more

### 🎨 Customization
- **3 Themes** — Dark, Light, and Classic
- **Premium Piece Sets** — 7 exclusive styles
- **Board Flip** — Auto-rotate for Black
- **Sound Effects** — Move, capture, check, checkmate, and more
- **Animations** — Smooth piece movements and visual effects

### 📊 Statistics & Progress
- **Win/Loss/Draw tracking** with visual donut chart
- **Elo rating system** (1200 starting, up to 3000)
- **Achievement system** — 30 unlockable achievements
- **Daily quests** — Complete missions for XP and gems
- **Game history** with move-by-move replay

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.13** | Core language |
| **PyQt5** | GUI framework |
| **python-chess** | Chess logic and move validation |
| **Stockfish** | AI opponent (optional) |
| **pygame** | Audio playback |
| **Pillow (PIL)** | Image processing |
| **QTcpSocket** | LAN multiplayer networking |

---

## 🚀 Installation

### For Players (Windows)

1. Download `CGACChess_Windows.zip` from [itch.io](https://mkiya.itch.io/cgacchess)
2. Extract the ZIP file
3. Run `CGACChess.exe`
4. No installation required!

### For Developers (Run from Source)

```bash
# 1. Clone the repository
git clone https://github.com/Mohammadkiya2012/CGACChess.git
cd CGACChess

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Download Stockfish engine
# Place stockfish.exe in the project root for stronger AI

# 4. Run the game
python main.py
PyQt5>=5.15.0
python-chess>=1.999
pygame>=2.5.0
Pillow>=10.0.0

🗺️ Roadmap
We have big plans for CGACChess! Here's what's coming:

☑ ~~v0.1.0 — Basic chess gameplay with AI~~
☑ ~~v0.2.0 — LAN multiplayer and daily challenges~~
☑ ~~v0.3.0 — Enhanced move history, lessons, and premium features~~ (current)
□ v0.1.0 (stable) — Community-driven improvements based on YOUR feedback
□ 2vs2 Chess Mode
□ 3-Player Chess (Hexagonal board)
□ 4-Player Chess (8-sided board)
□ Remote Online Multiplayer (requires server funding)
💡 Help us reach v0.1.0! Your feedback shapes the future of this game.

🤝 Contributing
This game is a Work in Progress, and it will only get better with YOUR feedback!

Every comment—whether it's praise, criticism, or even insults—is incredibly valuable to us. This is a game where YOU put the ideas.

How to contribute:
🐛 Report bugs — Open an Issue

💡 Suggest features — Start a Discussion

⭐ Star this repo — It helps others find the project

🍴 Fork & PR — Submit your own improvements

💎 Support Us
CGACChess is 100% free to play. If you'd like to support development:

⭐ Star this repository

🎮 Download and play the game on itch.io

📧 Donate via email (see itch.io page for details)

⚠️ Important Note:
Because we are based in Iran and face many sanctions, please do NOT donate via PayPal or any other platforms unavailable to Iranians. Contact us via email for alternative donation methods.

👨‍💻 Authors
M.Kiya — Lead Developer
Sobhan — Co-Developer
Average age: 14.5

📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

🌟 Acknowledgments
python-chess — Incredible chess library

Stockfish — Powerful open-source chess engine

PyQt5 — GUI framework

All our early players and testers 💙

📬 Contact
itch.io: mkiya.itch.io/cgacchess

GitHub: @Mohammadkiya2012

Email: mkiya.maleki@gmail.com, sobhanbavaghar.1319@gmail.com

<div align="center">
♔ Strategy • Intelligence • Victory ♚

Made with ❤️ in Iran 🇮🇷

⭐ If you like this project, please give it a star! ⭐
