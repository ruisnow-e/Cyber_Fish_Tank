CYBER FISH TANK
===============
> **Final Project for CS5001** 
> **Instructor: Professor Mark Miller**

An interactive AI-powered fish tank application where users draw their own fish, 
classify them with a machine learning model, and watch them swim inside a virtual tank. 
Users can also feed their fish and observe their reactions in the fishtank.

### Team Members
* **Zhuoying Xue**
* **Lai Jiang**
* **Rui Song**

--------------------------------------------------------------------------------
INSTALLATION & ENVIRONMENT SETUP
--------------------------------------------------------------------------------

1. Use Python 3.10
   This project requires Python 3.10, as TensorFlow 2.11 is not compatible with newer versions.

2. Create and Activate a Virtual Environment
   python3.10 -m venv tfenv
   source tfenv/bin/activate

3. Install Dependencies
   pip install -r requirements.txt

4. Install Tkinter (macOS Only)
   macOS may ship with an outdated Tk version. Install the correct Tk bindings for Python 3.10:
   brew install python-tk@3.10

--------------------------------------------------------------------------------
RUN THE APPLICATION
--------------------------------------------------------------------------------

Run the following command:
python main.py

--------------------------------------------------------------------------------
HOW IT WORKS
--------------------------------------------------------------------------------

- A Tkinter drawing interface opens, allowing the user to draw a fish.
- After the user submits the drawing, the system prompts them to enter a name for the fish.
- The drawing is saved into the fish_drawings/ folder.
- A machine learning classifier analyzes the drawing to determine the likelihood that it is a fish.
- The user is prompted to enter a specific swimming speed for their fish.
- The fish appears inside a virtual tank and swims around at the entered speed.
- Users can feed the fish using in-game controls and observe their behavior as they move toward food.

--------------------------------------------------------------------------------
FEATURES
--------------------------------------------------------------------------------

- Draw your own fish using a custom Tkinter drawing UI
- Custom fish naming system
- ML-based fish likelihood detection using Google Teachable Machine
- User-defined swimming speeds
- Animated fish tank built with Pygame
- Interactive feeding system with emoji-based food items
- Persistent fish drawing storage
- Background assets for customizable tanks

--------------------------------------------------------------------------------
PROJECT STRUCTURE
--------------------------------------------------------------------------------

.
├── main.py
├── drawing_interface.py
├── fish_classifier.py
├── converted_keras/      #AI model downloaded from Google Teachable Machine
│   ├── keras_model.h5
│   └── labels.txt
├── fishtank.py
├── food_images/          # emojis
├── fish_drawings/        # User drawings
├── tank/                 # Backgrounds
├── requirements.txt
└── README.md

--------------------------------------------------------------------------------
NOTES
--------------------------------------------------------------------------------

- Ensure your virtual environment runs Python 3.10.
- Tkinter version must match the Python version to avoid GUI compatibility issues.

--------------------------------------------------------------------------------
FUTURE IMPROVEMENTS
--------------------------------------------------------------------------------

- Multiplayer / shared fish tanks
- Global ranking system