import os
import pickle
import numpy as np
from tensorflow import keras
from typing import Tuple


def load_model(model_path: str):
    """Load the Keras model from .h5 file."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return keras.models.load_model(model_path)


def load_vectorizer(vectorizer_path: str):
    """Load the TF-IDF vectorizer from .pkl file."""
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
    with open(vectorizer_path, 'rb') as f:
        return pickle.load(f)


def predict_label(model, vectorizer, text: str) -> Tuple[str, float]:
    """
    Predict whether a job posting is real or fake.
    
    Args:
        model: Loaded Keras model
        vectorizer: Loaded TF-IDF vectorizer
        text: Job posting text to classify
    
    Returns:
        Tuple of (prediction_label, confidence_score)
        prediction_label: "real" or "fake"
        confidence_score: float between 0 and 1
    """
    # Vectorize the input text
    text_vectorized = vectorizer.transform([text])
    
    # Get prediction from model
    prediction = model.predict(text_vectorized, verbose=0)
    
    # Assuming binary classification: [probability_fake, probability_real] or single output
    # Adjust based on your model's output format
    if prediction.shape[1] == 2:
        # Binary classification with 2 outputs
        prob_fake, prob_real = prediction[0]
        confidence = max(prob_fake, prob_real)
        label = "fake" if prob_fake > prob_real else "real"
    else:
        # Single output (probability of fake, for example)
        prob = float(prediction[0][0])
        confidence = max(prob, 1 - prob)
        label = "fake" if prob > 0.5 else "real"
    
    return label, float(confidence)

