"""Utilities for loading the Udacity recruitment classifier."""

import pickle
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent
model_path = project_root / "assets" / "model.pkl"


def load_model():
    """Load the pretrained recruitment classifier supplied by Udacity."""
    if not model_path.is_file():
        raise FileNotFoundError(f"Prediction model not found: {model_path}")
    with model_path.open("rb") as model_file:
        return pickle.load(model_file)
