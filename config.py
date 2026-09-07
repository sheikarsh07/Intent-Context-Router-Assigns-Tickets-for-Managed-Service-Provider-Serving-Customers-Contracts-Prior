"""
Central Configuration for Intent + Context Router
All soft constraint weights, organizational policies, resolver definitions,
and file paths are centrally managed here.
"""

import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TESTS_DIR = os.path.join(BASE_DIR, "tests")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# Data File Paths
TICKETS_CSV = os.path.join(DATA_DIR, "tickets.csv")
ORGANIZATIONS_CSV = os.path.join(DATA_DIR, "organizations.csv")
RESOLVER_GROUPS_CSV = os.path.join(DATA_DIR, "resolver_groups.csv")
TEST_CASES_CSV = os.path.join(TESTS_DIR, "test_cases.csv")
METRICS_JSON = os.path.join(RESULTS_DIR, "metrics.json")
ERROR_ANALYSIS_CSV = os.path.join(RESULTS_DIR, "error_analysis.csv")

# Standard System Values
RESOLVER_GROUPS = [
    "Network Team",
    "Security Team",
    "Database Team",
    "Hardware Team",
    "Application Team",
    "Cloud Team"
]

PRIORITIES = ["Low", "Medium", "High", "Critical"]
CHANNELS = ["Portal", "Email", "Phone", "Chat"]
USER_ROLES = ["Employee", "Manager", "IT Admin", "Security Admin", "External Partner"]
CONTRACT_TYPES = ["Basic Support", "Standard Enterprise", "Premium SLA", "Mission Critical"]

ASSETS = [
    "Laptop",
    "Desktop",
    "VPN",
    "Database Server",
    "Cloud VM",
    "Application Server",
    "Network Device"
]

INTENTS = [
    "VPN Issue",
    "Database Outage",
    "Hardware Fault",
    "Security Incident",
    "Application Crash",
    "Cloud Outage"
]

# Primary Resolver mapping per intent & asset
INTENT_PRIMARY_RESOLVER = {
    "VPN Issue": "Network Team",
    "Database Outage": "Database Team",
    "Hardware Fault": "Hardware Team",
    "Security Incident": "Security Team",
    "Application Crash": "Application Team",
    "Cloud Outage": "Cloud Team"
}

ASSET_PRIMARY_RESOLVER = {
    "VPN": "Network Team",
    "Network Device": "Network Team",
    "Database Server": "Database Team",
    "Laptop": "Hardware Team",
    "Desktop": "Hardware Team",
    "Application Server": "Application Team",
    "Cloud VM": "Cloud Team"
}

# Configurable Soft Constraint Scoring Weights
SOFT_WEIGHTS = {
    "intent_match": 35.0,
    "asset_match": 25.0,
    "org_match": 10.0,
    "contract_compat": 10.0,
    "priority_compat": 5.0,
    "channel_compat": 5.0,
    "history_success": 10.0,
    "bounce_penalty": -30.0
}

