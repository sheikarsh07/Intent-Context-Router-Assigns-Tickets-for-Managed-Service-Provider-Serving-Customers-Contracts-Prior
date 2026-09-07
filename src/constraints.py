"""
Constraints & Scoring Engine Module (Phases 4 & 5)
Handles:
1. Hard Constraints: Filters out ineligible candidate resolver groups.
2. Soft Constraints: Calculates weighted compatibility scores for remaining candidates.
"""

import os
import sys
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config


class ConstraintEngine:
    """Manages hard filtering constraints and soft weighted scoring."""

    def __init__(self, orgs_csv=config.ORGANIZATIONS_CSV, resolvers_csv=config.RESOLVER_GROUPS_CSV):
        if os.path.exists(orgs_csv):
            self.orgs_df = pd.read_csv(orgs_csv).set_index("organization")
        else:
            self.orgs_df = None

        if os.path.exists(resolvers_csv):
            self.resolvers_df = pd.read_csv(resolvers_csv).set_index("resolver_group")
        else:
            self.resolvers_df = None

    def evaluate_hard_constraints(self, candidate_resolver: str, ticket_data: dict, intent_info: dict) -> tuple:
        """
        Evaluates hard constraints for a single candidate resolver group.
        Returns: (is_eligible: bool, rejection_reasons: list)
        """
        rejection_reasons = []

        intent = intent_info.get("detected_intent", "")
        ticket_text = ticket_data.get("ticket_text", "").lower()
        org_name = ticket_data.get("organization", "")
        user_role = ticket_data.get("user_role", "")
        priority = ticket_data.get("priority", "")

        # 1. Hard Constraint: Security-sensitive tickets require Security Team
        is_security_incident = (
            intent == "Security Incident" or 
            any(word in ticket_text for word in ["ransomware", "compromise", "phishing", "exfiltration", "exploit", "unauthorized access payload"])
        )
        if is_security_incident and candidate_resolver != "Security Team":
            rejection_reasons.append(
                f"Security Team required because ticket is security-sensitive (Detected Intent: '{intent}')."
            )

        # 2. Hard Constraint: Organization Allowed Resolvers Policy
        if self.orgs_df is not None and org_name in self.orgs_df.index:
            org_info = self.orgs_df.loc[org_name]
            allowed_resolvers_str = str(org_info.get("allowed_resolvers", ""))
            allowed_list = allowed_resolvers_str.split("|") if allowed_resolvers_str else config.RESOLVER_GROUPS
            
            if candidate_resolver not in allowed_list:
                rejection_reasons.append(
                    f"{candidate_resolver} rejected because customer organization '{org_name}' contract restricts this resolver group."
                )

            # 3. Hard Constraint: External Partner Restriction
            if user_role == "External Partner":
                partner_allowed_str = str(org_info.get("partner_allowed_resolvers", ""))
                partner_allowed_list = partner_allowed_str.split("|") if partner_allowed_str else config.RESOLVER_GROUPS
                if candidate_resolver not in partner_allowed_list:
                    rejection_reasons.append(
                        f"{candidate_resolver} rejected because External Partner role is not permitted to access this resolver group."
                    )

        # 4. Hard Constraint: Priority Capability Limits
        if self.resolvers_df is not None and candidate_resolver in self.resolvers_df.index:
            resolver_info = self.resolvers_df.loc[candidate_resolver]
            max_prio = str(resolver_info.get("max_priority_handled", "Critical"))
            if priority == "Critical" and max_prio == "High":
                rejection_reasons.append(
                    f"{candidate_resolver} rejected because it cannot handle Critical priority tickets (Max: {max_prio})."
                )

        is_eligible = (len(rejection_reasons) == 0)
        return is_eligible, rejection_reasons

    def calculate_soft_score(self, candidate_resolver: str, ticket_data: dict, intent_info: dict) -> dict:
        """
        Calculates soft constraint score breakdown for an eligible candidate.
        Returns: {total_score, breakdown, explanation_points}
        """
        weights = config.SOFT_WEIGHTS
        score_breakdown = {}
        explanation_points = []
        total_score = 0.0

        detected_intent = str(intent_info.get("detected_intent", ""))
        asset = str(ticket_data.get("asset", ""))
        if pd.isna(asset) or asset == "nan":
            asset = "Unknown"

        org_name = str(ticket_data.get("organization", ""))
        if pd.isna(org_name) or org_name == "nan":
            org_name = "Unknown"

        user_role = str(ticket_data.get("user_role", ""))
        if pd.isna(user_role) or user_role == "nan":
            user_role = "Employee"

        contract = str(ticket_data.get("contract", ""))
        priority = str(ticket_data.get("priority", ""))
        channel = str(ticket_data.get("channel", ""))


        previous_resolver = str(ticket_data.get("previous_resolver", "None"))
        if pd.isna(previous_resolver) or previous_resolver == "nan":
            previous_resolver = "None"

        assignment_history = str(ticket_data.get("assignment_history", "None"))
        if pd.isna(assignment_history) or assignment_history == "nan":
            assignment_history = "None"

        # 1. Intent Match (+35)
        primary_for_intent = config.INTENT_PRIMARY_RESOLVER.get(detected_intent, "")
        if candidate_resolver == primary_for_intent:
            score = weights["intent_match"]
            score_breakdown["intent_match"] = score
            total_score += score
            explanation_points.append(f"Intent match (+{score:.0f}): Handles detected intent '{detected_intent}'.")
        else:
            score_breakdown["intent_match"] = 0.0

        # 2. Asset Match (+25)
        primary_for_asset = config.ASSET_PRIMARY_RESOLVER.get(asset, "")
        if candidate_resolver == primary_for_asset:
            score = weights["asset_match"]
            score_breakdown["asset_match"] = score
            total_score += score
            explanation_points.append(f"Asset match (+{score:.0f}): Handles primary asset type '{asset}'.")
        else:
            score_breakdown["asset_match"] = 0.0

        # Policy Fallback Boost: If primary intent/asset team is restricted by Org policy or Partner role,
        # Application Team serves as approved fallback handler.
        if primary_for_intent != candidate_resolver and candidate_resolver == "Application Team":
            if self.orgs_df is not None and org_name in self.orgs_df.index:
                allowed_str = str(self.orgs_df.loc[org_name].get("allowed_resolvers", ""))
                partner_allowed_str = str(self.orgs_df.loc[org_name].get("partner_allowed_resolvers", ""))
                if primary_for_intent not in allowed_str.split("|") or (user_role == "External Partner" and primary_for_intent not in partner_allowed_str.split("|")):
                    total_score += 25.0
                    explanation_points.append("Policy Fallback (+25): Application Team designated for restricted org/partner services.")


        # 3. Organization Policy Match (+10)
        if self.orgs_df is not None and org_name in self.orgs_df.index:
            score = weights["org_match"]
            score_breakdown["org_match"] = score
            total_score += score
            explanation_points.append(f"Org match (+{score:.0f}): Approved team for '{org_name}'.")
        else:
            score_breakdown["org_match"] = 0.0

        # 4. Contract Compatibility (+10)
        if contract in ["Premium SLA", "Mission Critical"] and candidate_resolver in ["Security Team", "Cloud Team", "Database Team"]:
            score = weights["contract_compat"]
            score_breakdown["contract_compat"] = score
            total_score += score
            explanation_points.append(f"Contract compatibility (+{score:.0f}): Aligned with {contract} tier.")
        else:
            score_breakdown["contract_compat"] = 5.0
            total_score += 5.0

        # 5. Priority Compatibility (+5)
        if priority in ["High", "Critical"]:
            score = weights["priority_compat"]
            score_breakdown["priority_compat"] = score
            total_score += score
            explanation_points.append(f"Priority compatibility (+{score:.0f}): High capability for {priority} ticket.")
        else:
            score_breakdown["priority_compat"] = 3.0
            total_score += 3.0

        # 6. Channel Compatibility (+5)
        score_breakdown["channel_compat"] = weights["channel_compat"]
        total_score += weights["channel_compat"]

        # 7. Assignment History & Bounce Penalty (-30)
        history_teams = [t.strip() for t in assignment_history.split("->") if t.strip() and t.strip() != "None"]
        if previous_resolver != "None" and candidate_resolver == previous_resolver:
            penalty = weights["bounce_penalty"]
            score_breakdown["bounce_penalty"] = penalty
            total_score += penalty
            explanation_points.append(f"Previous bounce penalty ({penalty:.0f}): Ticket previously bounced from {candidate_resolver}.")
        elif candidate_resolver in history_teams:
            penalty = weights["bounce_penalty"]
            score_breakdown["bounce_penalty"] = penalty
            total_score += penalty
            explanation_points.append(f"History bounce penalty ({penalty:.0f}): {candidate_resolver} failed in prior attempt history ({assignment_history}).")
        else:
            score_breakdown["bounce_penalty"] = 0.0



        return {
            "total_score": max(0.0, total_score),
            "breakdown": score_breakdown,
            "explanation_points": explanation_points
        }
