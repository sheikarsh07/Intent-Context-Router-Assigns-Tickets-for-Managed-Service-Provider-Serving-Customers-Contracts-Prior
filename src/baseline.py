"""
Baseline Model Module (Phase 2)
Implements a simple text-only baseline classifier using TF-IDF and Logistic Regression / Naive Bayes.
The baseline routes tickets solely based on ticket_text without considering organization,
contract, priority, channel, asset, user role, or assignment history.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config



class BaselineRouter:
    """Text-only baseline classifier."""
    
    def __init__(self, model_type="logistic"):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        if model_type == "naive_bayes":
            self.model = MultinomialNB()
        else:
            self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.is_trained = False

    def train(self, df: pd.DataFrame):
        """Trains the baseline text classifier on ticket_text and correct_resolver."""
        X_text = df["ticket_text"].fillna("")
        y = df["correct_resolver"]
        
        X_tfidf = self.vectorizer.fit_transform(X_text)
        self.model.fit(X_tfidf, y)
        self.is_trained = True
        return self

    def predict(self, ticket_text: str) -> dict:
        """Predicts resolver group based purely on ticket text."""
        if not self.is_trained:
            raise ValueError("Baseline model is not trained yet.")

        X_tfidf = self.vectorizer.transform([ticket_text])
        predicted_resolver = self.model.predict(X_tfidf)[0]
        
        # Get prediction probabilities for confidence
        probabilities = self.model.predict_proba(X_tfidf)[0]
        classes = self.model.classes_
        confidence = float(np.max(probabilities))
        
        class_scores = {cls: float(prob) for cls, prob in zip(classes, probabilities)}

        return {
            "predicted_resolver": predicted_resolver,
            "confidence": confidence,
            "class_scores": class_scores,
            "model_type": "Baseline (TF-IDF Text Only)"
        }

    def predict_dataframe(self, df: pd.DataFrame) -> list:
        """Predicts resolver groups for a dataframe of tickets."""
        if not self.is_trained:
            raise ValueError("Baseline model is not trained yet.")
        
        X_tfidf = self.vectorizer.transform(df["ticket_text"].fillna(""))
        predictions = self.model.predict(X_tfidf)
        return list(predictions)
