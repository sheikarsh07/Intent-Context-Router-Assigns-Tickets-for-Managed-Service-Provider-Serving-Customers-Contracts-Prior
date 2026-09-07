"""
Data Generator Module (Phase 1)
Generates realistic synthetic data for organizations, resolver groups,
500+ support tickets, and adversarial test cases.
"""

import os
import sys
import random
import pandas as pd
import numpy as np

# Ensure parent directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config


def generate_organizations_csv():
    """Generates metadata for customer organizations and policies."""
    os.makedirs(config.DATA_DIR, exist_ok=True)
    orgs_data = [
        {
            "organization": "ABC Corp",
            "contract": "Standard Enterprise",
            "allowed_resolvers": "Network Team|Security Team|Database Team|Hardware Team|Application Team|Cloud Team",
            "partner_allowed_resolvers": "Network Team|Hardware Team|Application Team",
            "security_restricted": False,
            "max_priority": "Critical"
        },
        {
            "organization": "XYZ Ltd",
            "contract": "Basic Support",
            "allowed_resolvers": "Network Team|Security Team|Hardware Team|Application Team",
            "partner_allowed_resolvers": "Hardware Team|Application Team",
            "security_restricted": True,
            "max_priority": "High"
        },
        {
            "organization": "Acme Technologies",
            "contract": "Mission Critical",
            "allowed_resolvers": "Network Team|Security Team|Database Team|Hardware Team|Application Team|Cloud Team",
            "partner_allowed_resolvers": "Network Team|Security Team|Database Team|Hardware Team|Application Team|Cloud Team",
            "security_restricted": False,
            "max_priority": "Critical"
        },
        {
            "organization": "Global Finance Inc",
            "contract": "Premium SLA",
            "allowed_resolvers": "Network Team|Security Team|Database Team|Application Team|Cloud Team",
            "partner_allowed_resolvers": "Application Team|Network Team",
            "security_restricted": True,
            "max_priority": "Critical"
        }
    ]
    df = pd.DataFrame(orgs_data)
    df.to_csv(config.ORGANIZATIONS_CSV, index=False)
    print(f"Generated {len(df)} organizations at {config.ORGANIZATIONS_CSV}")
    return df


def generate_resolver_groups_csv():
    """Generates metadata and permission capabilities for resolver groups."""
    os.makedirs(config.DATA_DIR, exist_ok=True)
    resolvers_data = [
        {
            "resolver_group": "Network Team",
            "is_security_authorized": False,
            "handled_assets": "VPN|Network Device",
            "handled_intents": "VPN Issue",
            "max_priority_handled": "Critical"
        },
        {
            "resolver_group": "Security Team",
            "is_security_authorized": True,
            "handled_assets": "VPN|Laptop|Desktop|Database Server|Cloud VM|Application Server|Network Device",
            "handled_intents": "Security Incident",
            "max_priority_handled": "Critical"
        },
        {
            "resolver_group": "Database Team",
            "is_security_authorized": False,
            "handled_assets": "Database Server",
            "handled_intents": "Database Outage",
            "max_priority_handled": "Critical"
        },
        {
            "resolver_group": "Hardware Team",
            "is_security_authorized": False,
            "handled_assets": "Laptop|Desktop",
            "handled_intents": "Hardware Fault",
            "max_priority_handled": "High"
        },
        {
            "resolver_group": "Application Team",
            "is_security_authorized": False,
            "handled_assets": "Application Server|Laptop|Desktop",
            "handled_intents": "Application Crash",
            "max_priority_handled": "Critical"
        },
        {
            "resolver_group": "Cloud Team",
            "is_security_authorized": False,
            "handled_assets": "Cloud VM",
            "handled_intents": "Cloud Outage",
            "max_priority_handled": "Critical"
        }
    ]
    df = pd.DataFrame(resolvers_data)
    df.to_csv(config.RESOLVER_GROUPS_CSV, index=False)
    print(f"Generated {len(df)} resolver groups at {config.RESOLVER_GROUPS_CSV}")
    return df


def generate_tickets_csv(n_tickets=550, random_seed=42):
    """Generates synthetic tickets with realistic relationships, intent, context, and ground truth."""
    random.seed(random_seed)
    np.random.seed(random_seed)
    os.makedirs(config.DATA_DIR, exist_ok=True)

    intent_templates = {
        "VPN Issue": [
            "Cannot connect to corporate VPN from home network",
            "VPN tunnel dropping connection every few minutes",
            "Remote access gateway timeout during sign in",
            "VPN client giving authentication error 800",
            "Slow throughput over Cisco AnyConnect VPN connection"
        ],
        "Database Outage": [
            "Database connection pool exhausted on production server",
            "SQL query execution timing out for reporting service",
            "Database cluster replication delay critical alert",
            "Corrupted table index causing database deadlock",
            "PostgreSQL database service stopped unexpectedly"
        ],
        "Hardware Fault": [
            "Laptop screen flickering and going completely blank",
            "Desktop PC failing to POST hardware boot diagnostic",
            "Solid state drive reporting SMART disk failure error",
            "Overheating CPU causing laptop system thermal shutdown",
            "Keyboard and trackpad unresponsive on developer laptop"
        ],
        "Security Incident": [
            "Suspicious multiple failed login attempts from unknown IP address",
            "Ransomware threat notification detected on workstation",
            "Employee account compromised sending phishing emails",
            "Unauthorized privilege escalation attempt in active directory",
            "Potential data exfiltration alert triggered on firewall"
        ],
        "Application Crash": [
            "ERP software crashing upon submitting monthly invoice report",
            "Web portal throwing HTTP 500 internal server error",
            "Mobile app freezing on checkout payment screen",
            "CRM module memory leak causing severe slow response",
            "Desktop app crashing with unhandled null pointer exception"
        ],
        "Cloud Outage": [
            "AWS EC2 instance instance status check failed",
            "Azure Cloud VM unreachable via SSH connection",
            "Kubernetes pod crash loop backoff on cloud node",
            "Cloud storage bucket access permission denied",
            "Auto-scaling group failing to launch new cloud instances"
        ]
    }

    intent_asset_map = {
        "VPN Issue": ["VPN", "Network Device"],
        "Database Outage": ["Database Server"],
        "Hardware Fault": ["Laptop", "Desktop"],
        "Security Incident": ["Laptop", "Desktop", "VPN", "Database Server", "Cloud VM", "Application Server", "Network Device"],
        "Application Crash": ["Application Server", "Laptop", "Desktop"],
        "Cloud Outage": ["Cloud VM"]
    }

    orgs_info = {
        "ABC Corp": {"contract": "Standard Enterprise", "allowed": ["Network Team", "Security Team", "Database Team", "Hardware Team", "Application Team", "Cloud Team"]},
        "XYZ Ltd": {"contract": "Basic Support", "allowed": ["Network Team", "Security Team", "Hardware Team", "Application Team"]},
        "Acme Technologies": {"contract": "Mission Critical", "allowed": ["Network Team", "Security Team", "Database Team", "Hardware Team", "Application Team", "Cloud Team"]},
        "Global Finance Inc": {"contract": "Premium SLA", "allowed": ["Network Team", "Security Team", "Database Team", "Application Team", "Cloud Team"]}
    }

    roles = ["Employee", "Manager", "IT Admin", "Security Admin", "External Partner"]
    channels = ["Portal", "Email", "Phone", "Chat"]
    priorities = ["Low", "Medium", "High", "Critical"]

    tickets = []
    
    for i in range(1, n_tickets + 1):
        ticket_id = f"TCK-{1000 + i}"
        
        # Pick intent
        intent = random.choice(config.INTENTS)
        template_text = random.choice(intent_templates[intent])
        
        # Add slight natural language variation
        prefixes = ["URGENT: ", "Issue reported: ", "Help needed: ", "System Alert - ", "User inquiry: ", ""]
        ticket_text = random.choice(prefixes) + template_text
        
        # Determine correct resolver based on intent & hard constraint rules
        primary_target = config.INTENT_PRIMARY_RESOLVER[intent]
        
        # Pick Organization
        org = random.choice(list(orgs_info.keys()))
        contract = orgs_info[org]["contract"]
        allowed_teams = orgs_info[org]["allowed"]
        
        # Handle organization restriction override:
        if primary_target not in allowed_teams:
            # If the primary resolver is restricted for this org (e.g. Cloud/DB for XYZ Ltd or Hardware for Global Finance Inc),
            # the correct resolver defaults to Application Team or Network Team as per contract policy
            correct_resolver = "Application Team" if "Application Team" in allowed_teams else "Network Team"
        else:
            correct_resolver = primary_target
            
        # Role & Channel
        user_role = random.choice(roles)
        
        # External partner restriction check:
        if user_role == "External Partner":
            # External partners at XYZ Ltd or Global Finance Inc restricted
            if org in ["XYZ Ltd", "Global Finance Inc"] and correct_resolver not in ["Hardware Team", "Application Team"]:
                correct_resolver = "Application Team"
        
        # Security Incident MUST go to Security Team
        if intent == "Security Incident":
            correct_resolver = "Security Team"

        # Asset selection consistent with intent
        asset = random.choice(intent_asset_map[intent])
        
        # Priority selection (Security/Outages lean Higher)
        if intent in ["Security Incident", "Database Outage", "Cloud Outage"]:
            priority = random.choice(["Medium", "High", "Critical", "Critical"])
        else:
            priority = random.choice(priorities)
            
        channel = random.choice(channels)
        
        # Simulate realistic assignment history & bounce simulation
        # 75% tickets resolved 1st attempt; 25% have bounced previously
        has_bounced = random.random() < 0.25
        if has_bounced:
            assignment_count = random.randint(2, 4)
            # Wrong previous resolvers that caused the bounce
            possible_wrong = [r for r in config.RESOLVER_GROUPS if r != correct_resolver]
            previous_resolver = random.choice(possible_wrong)
            history_list = []
            for _ in range(assignment_count - 1):
                history_list.append(random.choice(possible_wrong))
            history_str = " -> ".join(history_list)
        else:
            assignment_count = 1
            previous_resolver = "None"
            history_str = "None"

        tickets.append({
            "ticket_id": ticket_id,
            "ticket_text": ticket_text,
            "intent": intent,
            "organization": org,
            "contract": contract,
            "priority": priority,
            "channel": channel,
            "asset": asset,
            "user_role": user_role,
            "previous_resolver": previous_resolver,
            "assignment_history": history_str,
            "assignment_count": assignment_count,
            "correct_resolver": correct_resolver
        })

    df_tickets = pd.DataFrame(tickets)
    df_tickets.to_csv(config.TICKETS_CSV, index=False)
    print(f"Generated {len(df_tickets)} support tickets at {config.TICKETS_CSV}")
    return df_tickets


def generate_test_cases_csv():
    """Generates at least 10 adversarial and edge test cases."""
    os.makedirs(config.TESTS_DIR, exist_ok=True)
    test_cases = [
        {
            "case_id": "ADV-01",
            "name": "Misleading Keywords (VPN word in Application ticket)",
            "ticket_text": "Need help logging into the financial ERP application over VPN connection",
            "organization": "ABC Corp",
            "contract": "Standard Enterprise",
            "priority": "Medium",
            "channel": "Portal",
            "asset": "Application Server",
            "user_role": "Employee",
            "previous_resolver": "Network Team",
            "assignment_history": "Network Team",
            "expected_resolver": "Application Team",
            "category": "Misleading Text / History Signal",
            "notes": "Text mentions VPN, but asset is Application Server and previous Network Team bounced."
        },
        {
            "case_id": "ADV-02",
            "name": "Security Issue Disguised as Database Query Error",
            "ticket_text": "SQL database error: unauthorized access payload detected in user input parameter",
            "organization": "Acme Technologies",
            "contract": "Mission Critical",
            "priority": "Critical",
            "channel": "Portal",
            "asset": "Database Server",
            "user_role": "Security Admin",
            "previous_resolver": "None",
            "assignment_history": "None",
            "expected_resolver": "Security Team",
            "category": "Hard Constraint (Security)",
            "notes": "Mentions database SQL, but contains security exploit payload; hard constraint requires Security Team."
        },
        {
            "case_id": "ADV-03",
            "name": "Organization Does Not Permit Cloud Team",
            "ticket_text": "Cloud VM instance crashing on reboot",
            "organization": "XYZ Ltd",
            "contract": "Basic Support",
            "priority": "High",
            "channel": "Email",
            "asset": "Cloud VM",
            "user_role": "Employee",
            "previous_resolver": "None",
            "assignment_history": "None",
            "expected_resolver": "Application Team",
            "category": "Hard Constraint (Org Policy)",
            "notes": "XYZ Ltd does not permit Cloud Team under Basic Support contract; falls back to Application Team."
        },
        {
            "case_id": "ADV-04",
            "name": "External Partner Restriction on Security Operations",
            "ticket_text": "Requesting password reset for external contractor account on database",
            "organization": "Global Finance Inc",
            "contract": "Premium SLA",
            "priority": "Medium",
            "channel": "Portal",
            "asset": "Database Server",
            "user_role": "External Partner",
            "previous_resolver": "None",
            "assignment_history": "None",
            "expected_resolver": "Application Team",
            "category": "Hard Constraint (Partner Restriction)",
            "notes": "External partner restricted from direct Database Team assignment at Global Finance Inc."
        },
        {
            "case_id": "ADV-05",
            "name": "Previous Resolver Wrong (Avoid Bounce Trap)",
            "ticket_text": "VPN tunnel disconnects every 10 minutes",
            "organization": "ABC Corp",
            "contract": "Standard Enterprise",
            "priority": "High",
            "channel": "Phone",
            "asset": "VPN",
            "user_role": "Manager",
            "previous_resolver": "Application Team",
            "assignment_history": "Application Team -> Hardware Team",
            "expected_resolver": "Network Team",
            "category": "Bounce Avoidance",
            "notes": "Application & Hardware teams failed earlier; router must assign to Network Team despite history."
        },
        {
            "case_id": "ADV-06",
            "name": "Missing Asset Information",
            "ticket_text": "Laptop screen flickering and system hardware thermal shutdown",
            "organization": "ABC Corp",
            "contract": "Standard Enterprise",
            "priority": "Low",
            "channel": "Chat",
            "asset": "Unknown",
            "user_role": "Employee",
            "previous_resolver": "None",
            "assignment_history": "None",
            "expected_resolver": "Hardware Team",
            "category": "Missing Context",
            "notes": "Missing asset relies on intent detection and hardware default."
        },

        {
            "case_id": "ADV-07",
            "name": "Missing Organization Information",
            "ticket_text": "PostgreSQL database query timing out",
            "organization": "Unknown",
            "contract": "Unknown",
            "priority": "High",
            "channel": "Email",
            "asset": "Database Server",
            "user_role": "IT Admin",
            "previous_resolver": "None",
            "assignment_history": "None",
            "expected_resolver": "Database Team",
            "category": "Missing Context",
            "notes": "Missing organization defaults to open permissions while scoring Database Team high based on asset/text."
        },
        {
            "case_id": "ADV-08",
            "name": "Critical Ticket Requiring Authorized Resolver",
            "ticket_text": "Ransomware pop-up warning on domain controller server",
            "organization": "Global Finance Inc",
            "contract": "Premium SLA",
            "priority": "Critical",
            "channel": "Phone",
            "asset": "Application Server",
            "user_role": "Security Admin",
            "previous_resolver": "Hardware Team",
            "assignment_history": "Hardware Team",
            "expected_resolver": "Security Team",
            "category": "Hard Constraint (Priority + Security)",
            "notes": "Ransomware critical alert strictly forces Security Team."
        },
        {
            "case_id": "ADV-09",
            "name": "Conflicting Context Fields (Laptop Asset vs Cloud Outage Text)",
            "ticket_text": "Cloud VM instance unresponsive after reboot script",
            "organization": "Acme Technologies",
            "contract": "Mission Critical",
            "priority": "High",
            "channel": "Portal",
            "asset": "Laptop",
            "user_role": "Employee",
            "previous_resolver": "None",
            "assignment_history": "None",
            "expected_resolver": "Cloud Team",
            "category": "Conflicting Context",
            "notes": "Text intent strongly points to Cloud VM over user laptop asset."
        },
        {
            "case_id": "ADV-10",
            "name": "Ambiguous Intent with Low Confidence",
            "ticket_text": "Please check status of request",
            "organization": "ABC Corp",
            "contract": "Standard Enterprise",
            "priority": "Low",
            "channel": "Chat",
            "asset": "Unknown",
            "user_role": "Employee",
            "previous_resolver": "None",
            "assignment_history": "None",
            "expected_resolver": "Application Team",
            "category": "Ambiguous / Low Confidence",
            "notes": "Text contains no clear technical keywords; should trigger low confidence recommendation."
        }
    ]
    df = pd.DataFrame(test_cases)
    df.to_csv(config.TEST_CASES_CSV, index=False)
    print(f"Generated {len(df)} test cases at {config.TEST_CASES_CSV}")
    return df


if __name__ == "__main__":
    generate_organizations_csv()
    generate_resolver_groups_csv()
    generate_tickets_csv()
    generate_test_cases_csv()
