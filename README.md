# 🐟 CyberFishTank

An interactive AI-powered virtual fish tank — draw your own fish, let a machine learning model judge how fish-like it looks, then watch it swim, chase food, and blow bubbles in a Pygame aquarium.

> Final Project for **CS5001** · Northeastern University MSCS · Fall 2025
> 
> Built by **Rui Song**, **Zhuoying Xue**, and **Lai Jiang**

---

## Demo

```
Draw a fish  →  AI rates it  →  Watch it swim
```

1. A Tkinter canvas opens — draw anything you like
2. Name your fish and set its swimming speed (1–5)
3. The ML classifier scores how fish-like your drawing is
4. Your fish appears in the aquarium alongside all previously drawn fish
5. Press number keys `0–9` to drop different emoji food, watch fish chase it

---

## Features

- **Custom drawing interface** — freehand canvas with color palette, adjustable brush size, undo, and clear
- **AI fish classifier** — Google Teachable Machine model scores each drawing's fish-likeness (confidence 0–100%)
- **Persistent fish** — every drawing is saved to `fish_drawings/`; all past fish reappear each session
- **Animated aquarium** — fish swim, bounce off walls, and home in on the nearest food item
- **Emoji food system** — press `0–9` to drop different foods; fish chase and eat them with a fade animation
- **Bubble animation** — rising bubbles generated continuously from the tank floor
- **Switchable backgrounds** — press `←` / `→` arrow keys to cycle through tank backgrounds
- **Per-fish speed control** — set each fish's speed independently at launch

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Drawing UI | Tkinter |
| Aquarium Engine | Pygame |
| ML Classifier | TensorFlow 2.11 + Google Teachable Machine |
| Image Processing | Pillow (PIL) |
| Numerical Compute | NumPy |

---

## Getting Started

### Prerequisites

- Python **3.10** (required — TensorFlow 2.11 is not compatible with newer versions)
- macOS, Linux, or Windows

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-repo/CyberFishTank.git
cd CyberFishTank

# 2. Create a Python 3.10 virtual environment
python3.10 -m venv tfenv
source tfenv/bin/activate        # Windows: tfenv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. macOS only — fix Tkinter compatibility
brew install python-tk@3.10
```

### Run

```bash
python main.py
```

---

## How to Play

| Action | Control |
|---|---|
| Draw fish | Mouse drag on canvas |
| Change brush color | Click color swatch |
| Adjust brush size | Drag the brush size slider |
| Undo last stroke | Click **Undo** |
| Clear canvas | Click **Clear** |
| Submit drawing | Click **Submit (Save & Close)** |
| Drop food in tank | Press number keys `0`–`9` |
| Switch background | Press `←` / `→` arrow keys |
| Quit | Close the Pygame window |

---

## Project Structure

```
CyberFishTank/
├── main.py                  # Entry point — orchestrates the full flow
├── drawing_interface.py     # Tkinter freehand drawing canvas
├── fish_classifier.py       # TensorFlow ML classifier (fish vs. not fish)
├── fishtank.py              # Pygame aquarium engine (Fish, Bubble, Food, AquariumGame)
├── converted_keras/
│   ├── keras_model.h5       # Trained Teachable Machine model
│   └── labels.txt           # Class labels (Fish / Not Fish)
├── fish_drawings/           # Saved user drawings (auto-created)
├── food_images/             # Emoji food PNGs (🐟 🍕 🥐 🍤 …)
├── tank/                    # Aquarium background images
└── requirements.txt
```

---

## Architecture

```
main.py
  │
  ├─► drawing_interface.py   # Step 1 — user draws and names a fish
  │         └─ saves PNG to fish_drawings/
  │
  ├─► fish_classifier.py     # Step 2 — ML model scores the drawing
  │         └─ returns (is_fish: bool, confidence: float)
  │
  └─► fishtank.py            # Step 3 — Pygame aquarium launches
            ├─ Fish      — swims, bounces, chases food
            ├─ Bubble    — rises with random drift
            ├─ Food      — placed on click, fades when eaten
            └─ AquariumGame — main loop (60 fps)
```

---

## Team

| Name | Contributions |
|---|---|
| **Rui Song** | Pygame aquarium engine (`fishtank.py`), fish swimming & food-chasing logic, bubble animation, background switching |
| **Zhuoying Xue** | Tkinter drawing interface (`drawing_interface.py`), brush/color/undo system, transparent PNG export |
| **Lai Jiang** | ML classifier integration (`fish_classifier.py`), Teachable Machine model training, image preprocessing pipeline |

---

## Known Limitations

- Requires exactly **Python 3.10** due to TensorFlow 2.11 compatibility
- macOS users need to install `python-tk@3.10` separately via Homebrew
- `fish_drawings/` accumulates all past drawings — clear the folder manually to start fresh

---

## Future Improvements

- [ ] Multiplayer / shared fish tanks
- [ ] Global fish ranking system
- [ ] Export tank as GIF or video
- [ ] Web version (remove desktop dependency)

---

## License

MIT License · © 2025 CyberFishTank Team