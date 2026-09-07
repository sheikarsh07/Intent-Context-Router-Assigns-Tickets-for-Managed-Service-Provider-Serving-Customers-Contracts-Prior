"""
Intent Classifier Module (Phase 2 & 3)
Classifies ticket text into technical intent categories:
- VPN Issue -> Network Team
- Database Outage -> Database Team
- Hardware Fault -> Hardware Team
- Security Incident -> Security Team
- Application Crash -> Application Team
- Cloud Outage -> Cloud Team
Includes a security keyword interceptor for safety.
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
    """TF-IDF + Logistic Regression Text Intent Classifier."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.is_trained = False

    def train(self, df: pd.DataFrame):
        """Trains intent model on ticket_text -> intent."""
        X_text = df["ticket_text"].fillna("")
        y_intents = df["intent"]

        X_tfidf = self.vectorizer.fit_transform(X_text)
        self.model.fit(X_tfidf, y_intents)
        self.is_trained = True
        return self

    def predict_intent(self, ticket_text: str) -> dict:
        """Predicts technical intent and primary target resolver group."""
        if not self.is_trained:
            # Safe default fallback
            return {
                "detected_intent": "Application Crash",
                "confidence": 0.50,
                "primary_resolver": "Application Team"
            }

        # 1. Machine Learning Text Prediction
        X_tfidf = self.vectorizer.transform([ticket_text])
        predicted_intent = self.model.predict(X_tfidf)[0]
        probabilities = self.model.predict_proba(X_tfidf)[0]
        confidence = float(np.max(probabilities))
        primary_resolver = config.INTENT_PRIMARY_RESOLVER.get(predicted_intent, "Application Team")

        # 2. Security Interceptor Rule: Override if critical threat keywords appear
        security_keywords = ["ransomware", "compromise", "phishing", "exfiltration", "exploit", "unauthorized"]
        text_lower = ticket_text.lower()
        if any(keyword in text_lower for keyword in security_keywords):
            predicted_intent = "Security Incident"
            confidence = max(confidence, 0.95)
            primary_resolver = "Security Team"

        return {
            "detected_intent": predicted_intent,
            "confidence": confidence,
            "primary_resolver": primary_resolver
        }
