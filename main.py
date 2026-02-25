import os
import glob
from tkinter import simpledialog, messagebox

import drawing_interface
import fishtank
from fish_classifier import FishClassifier


def main():
    """ Folder setup """
    FISH_FOLDER = "fish_drawings"
    BG_FOLDER = "tank"
    os.makedirs(FISH_FOLDER, exist_ok=True)
    os.makedirs(BG_FOLDER, exist_ok=True)

    """ Step 1: Draw fish """
    print("Step 1: Draw your fish in the Tkinter window...")
    drawing_interface.main()  # waits until window closes

    """ Step 2: Get latest fish """
    latest_path = drawing_interface.get_drawing_image()
    latest_name = drawing_interface.get_drawing_name() or "Unnamed Fish"

    if not latest_path:
        print("No fish image found. Exiting...")
        return

    """ Step 3: AI classifier """
    classifier = FishClassifier()
    _, confidence = classifier.is_fish(latest_path)

    # Show fish recognition info in popup window
    messagebox.showinfo(
        "Fish Recognition",
        f"Latest fish: {latest_name}\n"
        f"AI estimates it is {confidence*100:.1f}% fish-like.\n\n"
        f"Click OK to continue."
    )

    """ Step 4: Load all historical fish """
    all_fish = sorted(
        [os.path.abspath(p) for p in glob.glob(os.path.join(FISH_FOLDER, "*.png"))],
        key=os.path.getctime
    )
    latest_abs = os.path.abspath(latest_path)

    # Remove duplicate if exists
    history_fish = [f for f in all_fish if f != latest_abs]

    # Final fish list: history + latest
    fish_images = history_fish + [latest_abs]

    """ Step 5: Ask speed only for latest fish """
    speed = simpledialog.askinteger(
        f"Set Speed for {latest_name}",
        f"Enter swimming speed for {latest_name} (1~5):",
        minvalue=1, maxvalue=5
    )
    if speed is None:
        speed = 2  # default

    # Speeds for all fish: history default 2, latest user-selected
    fish_speeds = [2] * len(history_fish) + [speed]

    """ Step 6: Launch fishtank """
    print("Launching fishtank with:", fish_images)
    fishtank.aquarium(
        fish_images=fish_images,
        fish_speeds=fish_speeds,
        fish_folder=FISH_FOLDER,
        bg_folder=BG_FOLDER
    )


if __name__ == "__main__":
    main()
