"""
Context-Aware Routing Engine (Phases 4, 5, 6)
Implements end-to-end transparent ticket routing pipeline:
1. Intent Detection
2. Candidate Resolver Generation
3. Hard Constraint Filtering
4. Soft Constraint Weighted Scoring
5. Winner Selection & Confidence Assessment
6. Explainable Decision Generation
"""

import os
import sys
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config
from src.intent import IntentClassifier
from src.constraints import ConstraintEngine


class ContextAwareRouter:
    """Context-aware router taking text + full operational context."""

    def __init__(self, df_train: pd.DataFrame = None):
        self.intent_classifier = IntentClassifier()
        self.constraint_engine = ConstraintEngine()
        self.is_trained = False
        
        if df_train is not None:
            self.train(df_train)

    def train(self, df_train: pd.DataFrame):
        """Trains intent classifier on historical tickets."""
        self.intent_classifier.train(df_train)
        self.is_trained = True
        return self

    def route_ticket(self, ticket_data: dict) -> dict:
        """
        Main routing function. Accepts dictionary containing ticket fields:
        - ticket_text
        - organization
        - contract
        - priority
        - channel
        - asset
        - user_role
        - previous_resolver
        - assignment_history
        """
        ticket_text = ticket_data.get("ticket_text", "")
        previous_resolver = str(ticket_data.get("previous_resolver", "None"))
        assignment_history = str(ticket_data.get("assignment_history", "None"))

        # Step 1: Detect Intent from text
        intent_info = self.intent_classifier.predict_intent(ticket_text)
        detected_intent = intent_info["detected_intent"]
        intent_confidence = intent_info["confidence"]

        # Step 2: Evaluate Hard & Soft Constraints across all Resolver Groups
        hard_constraints_evaluated = {}
        soft_constraints_applied = {}
        eligible_candidates = []
        scores_map = {}
        explanations_map = {}

        for resolver in config.RESOLVER_GROUPS:
            is_eligible, rejection_reasons = self.constraint_engine.evaluate_hard_constraints(
                resolver, ticket_data, intent_info
            )
            hard_constraints_evaluated[resolver] = {
                "is_eligible": is_eligible,
                "rejection_reasons": rejection_reasons
            }

            if is_eligible:
                eligible_candidates.append(resolver)
                soft_result = self.constraint_engine.calculate_soft_score(
                    resolver, ticket_data, intent_info
                )
                score = soft_result["total_score"]
                scores_map[resolver] = score
                soft_constraints_applied[resolver] = soft_result["breakdown"]
                explanations_map[resolver] = soft_result["explanation_points"]
            else:
                scores_map[resolver] = 0.0
                soft_constraints_applied[resolver] = {}

        # Step 3: Selection & Fallback Logic
        if not eligible_candidates:
            # Fallback if all candidates are hard-constrained
            selected_resolver = "Application Team"
            confidence = 0.30
            confidence_status = "Low Confidence — manual review recommended (All candidates hard-constrained)"
            explanation_summary = "All candidate resolver groups violated hard constraints. Defaulting to Application Team for manual triage."
            bounce_avoided = False
        else:
            # Rank eligible candidates by total score
            sorted_candidates = sorted(eligible_candidates, key=lambda x: scores_map[x], reverse=True)
            selected_resolver = sorted_candidates[0]
            top_score = scores_map[selected_resolver]

            # Calculate confidence score based on top score and score separation
            if len(sorted_candidates) > 1:
                second_score = scores_map[sorted_candidates[1]]
                margin = top_score - second_score
            else:
                margin = top_score

            # Normalize confidence (0.0 - 1.0)
            raw_conf = (top_score / 85.0) * 0.60 + (intent_confidence * 0.40)
            confidence = float(np.clip(raw_conf, 0.35, 0.99))

            if confidence >= 0.75:
                confidence_status = "High Confidence"
            elif confidence >= 0.55:
                confidence_status = "Medium Confidence"
            else:
                confidence_status = "Low Confidence — manual review recommended"

            # Check if assignment history was considered and bounce avoided
            history_str = assignment_history + " " + previous_resolver
            previous_assignment_considered = (previous_resolver != "None" or assignment_history != "None")
            bounce_avoided = (previous_resolver in config.RESOLVER_GROUPS and selected_resolver != previous_resolver)

            # Build explainable natural language explanation
            points = explanations_map.get(selected_resolver, [])
            explanation_lines = [
                f"**{selected_resolver}** selected as best match (Score: {top_score:.1f}/85.0):",
            ]
            for idx, pt in enumerate(points, 1):
                explanation_lines.append(f"  {idx}. {pt}")
            
            explanation_lines.append("  - No hard constraints were violated for this selection.")
            
            # Mention rejected candidates if any
            rejected_teams = [r for r, info in hard_constraints_evaluated.items() if not info["is_eligible"]]
            if rejected_teams:
                rejection_summary = ", ".join([f"{r} ({hard_constraints_evaluated[r]['rejection_reasons'][0]})" for r in rejected_teams])
                explanation_lines.append(f"\n*Hard constraints rejected*: {rejection_summary}")

            explanation_summary = "\n".join(explanation_lines)

        return {
            "selected_resolver": selected_resolver,
            "confidence": confidence,
            "confidence_status": confidence_status,
            "detected_intent": detected_intent,
            "intent_confidence": intent_confidence,
            "candidate_scores": scores_map,
            "eligible_candidates": eligible_candidates,
            "hard_constraints_evaluated": hard_constraints_evaluated,
            "soft_constraints_applied": soft_constraints_applied,
            "explanation": explanation_summary,
            "previous_assignment_considered": (previous_resolver != "None" or assignment_history != "None"),
            "bounce_avoided": bounce_avoided
        }

    def route_dataframe(self, df: pd.DataFrame) -> list:
        """Helper to route a full dataframe of tickets."""
        results = []
        for _, row in df.iterrows():
            ticket_dict = row.to_dict()
            res = self.route_ticket(ticket_dict)
            results.append(res["selected_resolver"])
        return results
