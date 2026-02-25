"""
fish_classifier.py

This module provides the AI classification component for our project. 
It loads a Teachable Machine model and builds a FishClassifier class 
that determines whether a drawing should be classified as a "Fish."

The classifier performs the following steps:
1. Loads the trained neural network model and its associated labels.
2. Cleans and normalizes label names (e.g., converting "0 Fish" → "Fish").
3. Automatically locates the correct index for the "Fish" class.
4. Preprocesses input images to match the model's required format
   (RGB, 224×224 pixels, normalized to [-1, 1]).
5. Runs the model prediction and returns:
      - a boolean indicating whether the input is a fish
      - the confidence score from the model
"""

from tensorflow.keras.models import load_model
from PIL import Image, ImageOps 
import numpy as np

import tkinter as tk
from tkinter import messagebox


def clean_label(raw: str) -> str:
    """
    Convert raw label lines like '0 Fish' or '1 Not Fish\n'
    into clean labels like 'Fish' or 'Not Fish'.
    """
    raw = raw.strip()  # remove whitespace & newline
    parts = raw.split(" ", 1)
    if len(parts) == 2:
        return parts[1]
    return parts[0]


class FishClassifier:
    def __init__(self,
                 model_path="converted_keras/keras_model.h5",
                 label_path="converted_keras/labels.txt",
                 threshold=0.20):
        """
        Initialize classifier, load model and labels once.
        threshold: default minimum confidence for accepting a fish
        """
        self.threshold = threshold

        # Load model
        self.model = load_model(model_path, compile=False)

        # Load and clean labels
        with open(label_path, "r") as f:
            self.class_names = [clean_label(line) for line in f.readlines()]

         # Find index of the 'Fish' label （defensive programming）
        if "Fish" not in self.class_names:
            raise ValueError("No 'Fish' class found in labels.txt")

        self.fish_index = self.class_names.index("Fish")



    def is_fish(self, image_path: str, show_popup = False):
        """
        Classify an image as Fish / Not Fish.
        Returns:
                (is_fish_flag: bool, confidence: float)
        """

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Load and preprocess
        image = Image.open(image_path).convert("RGB")
        image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
        image_array = np.asarray(image)

        # Normalize to [-1, 1]
        normalized_image = (image_array.astype(np.float32) / 127.5) - 1.0
        data[0] = normalized_image

        prediction = self.model.predict(data)
        confidence = float(prediction[0][self.fish_index])

        is_fish_flag = confidence >= self.threshold

        # Show popup: Probability of fish if show_popup is True
        if show_popup:
            root = tk.Tk()
            root.withdraw()  # hide empty root window

            msg = (
                f"Fish Probability: {confidence:.3f}\n\n"
                f"{'✔ This is a fish!' if is_fish_flag else '✘ Not a fish.'}"
            )
            messagebox.showinfo("AI Classification Result", msg)

        return is_fish_flag, confidence


if __name__ == "__main__":
    # import sys
    classifier = FishClassifier(threshold=0.20)
    # test a fish image
    img_path = "test_fish/fish_1.png"
    is_fish, conf = classifier.is_fish(img_path)

    print(is_fish, conf)

