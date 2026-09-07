"""
Intent Classification Engine (Phase 3)
Classifies ticket text into technical intent categories:
- VPN Issue
- Database Outage
- Hardware Fault
- Security Incident
- Application Crash
- Cloud Outage
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config



class IntentClassifier:
    """TF-IDF + Logistic Regression Intent Classifier."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.is_trained = False

    def train(self, df: pd.DataFrame):
        """Trains intent classifier on ticket_text -> intent label."""
        X_text = df["ticket_text"].fillna("")
        y = df["intent"]
        
        X_tfidf = self.vectorizer.fit_transform(X_text)
        self.model.fit(X_tfidf, y)
        self.is_trained = True
        return self

    def predict_intent(self, ticket_text: str) -> dict:
        """Predicts technical intent from ticket text."""
        if not self.is_trained:
            # Fallback if not trained
            return {
                "detected_intent": "Application Crash",
                "confidence": 0.50,
                "intent_scores": {intent: 1.0 / len(config.INTENTS) for intent in config.INTENTS},
                "primary_resolver": "Application Team"
            }

        X_tfidf = self.vectorizer.transform([ticket_text])
        predicted_intent = self.model.predict(X_tfidf)[0]
        
        probabilities = self.model.predict_proba(X_tfidf)[0]
        classes = self.model.classes_
        confidence = float(np.max(probabilities))
        
        intent_scores = {cls: float(prob) for cls, prob in zip(classes, probabilities)}
        primary_resolver = config.INTENT_PRIMARY_RESOLVER.get(predicted_intent, "Application Team")

        # Security keyword rule check to ensure security threats are never missed by text classifier alone
        security_keywords = ["ransomware", "compromise", "phishing", "exfiltration", "unauthorized", "exploit", "hack", "threat"]
        text_lower = ticket_text.lower()
        if any(kw in text_lower for kw in security_keywords):
            predicted_intent = "Security Incident"
            confidence = max(confidence, 0.95)
            primary_resolver = "Security Team"

        return {
            "detected_intent": predicted_intent,
            "confidence": confidence,
            "intent_scores": intent_scores,
            "primary_resolver": primary_resolver
        }
