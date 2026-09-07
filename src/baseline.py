"""
Baseline Model Module (Phase 2)
Implements a simple text-only baseline classifier using TF-IDF + Logistic Regression.
This model routes tickets purely based on ticket text without operational context.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Add parent directory to sys.path for config import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config


class BaselineRouter:
    """Text-only baseline routing classifier."""

    def __init__(self, model_type: str = "logistic"):
        # TF-IDF Vectorizer converts text into numerical feature matrix
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        # Logistic Regression predicts the target resolver group
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.is_trained = False


    def train(self, df: pd.DataFrame):
        """Trains the baseline classifier on ticket_text -> correct_resolver."""
        X_text = df["ticket_text"].fillna("")
        y_labels = df["correct_resolver"]

        # 1. Transform text to numerical vectors
        X_tfidf = self.vectorizer.fit_transform(X_text)
        
        # 2. Fit classifier model
        self.model.fit(X_tfidf, y_labels)
        self.is_trained = True
        return self

    def predict(self, ticket_text: str) -> dict:
        """Predicts resolver team for a single ticket string."""
        if not self.is_trained:
            raise ValueError("Baseline model must be trained before calling predict().")

        # Transform single input text
        X_tfidf = self.vectorizer.transform([ticket_text])
        predicted_team = self.model.predict(X_tfidf)[0]
        
        # Calculate prediction probability for confidence
        probabilities = self.model.predict_proba(X_tfidf)[0]
        confidence = float(np.max(probabilities))

        return {
            "predicted_resolver": predicted_team,
            "confidence": confidence,
            "model_type": "Baseline (Text-Only TF-IDF)"
        }

    def predict_dataframe(self, df: pd.DataFrame) -> list:
        """Predicts resolver teams for a full dataframe of tickets."""
        if not self.is_trained:
            raise ValueError("Baseline model must be trained before calling predict_dataframe().")

        X_tfidf = self.vectorizer.transform(df["ticket_text"].fillna(""))
        predictions = self.model.predict(X_tfidf)
        return list(predictions)
