# Intent + Context Router for Managed-Service Provider Ticket Assignment

> **Academic Software Prototype**: An explainable, context-aware IT support ticket routing engine that combines natural language text intent classification with operational hard/soft constraints to optimize first-assignment accuracy and reduce ticket bouncing.

> 📘 **VIVA PREPARATION GUIDE**: For a complete beginner-friendly breakdown of all algorithms, code functions, "Why & Why Not" choices, and viva Q&A, open [COMPLETE_PROJECT_GUIDE.docx](file:///f:/COE%20Project/COMPLETE_PROJECT_GUIDE.docx).

---


## 1. Project Title & Problem Statement

**Title**: *Intent Context Router Assigns Tickets for Managed-Service Provider Serving Customers' Contracts and Priorities*

### Problem Statement
In Managed-Service Provider (MSP) IT operations, incoming support tickets are traditionally routed based on basic text keywords or simple text classifiers. However, text alone lacks operational awareness. For example:
- A ticket mentioning "VPN" might actually be an **Application crash** occurring while the user is connected to VPN.
- A **Security incident** disguised as a database query error might be misassigned to the Database Team instead of the Security Team.
- Customer organization contracts, user roles (e.g. External Partners), and previous failed assignment histories are ignored, causing **ticket bouncing** (repeated reassignment between teams), increased mean-time-to-resolution (MTTR), and SLA breaches.

---

## 2. Main Objective & Proposed Solution

### Objectives
1. **Improve First-Assignment Accuracy**: Assign support tickets to the correct resolver team on the very first attempt.
2. **Reduce Ticket Bouncing**: Prevent tickets from being repeatedly shuffled between resolver teams.
3. **Respect Operational Constraints**: Enforce hard business rules (e.g. security authorizations, customer contract restrictions, partner access limits).
4. **Transparent Explainability**: Provide clear, human-readable explanations detailing why a specific resolver group was selected or rejected.
5. **Measurable Comparison**: Quantify improvements against a text-only baseline classifier.

### Proposed Architecture
The proposed system implements a multi-stage routing pipeline:
```
  [ Support Ticket Input ]
            │
            ▼
┌──────────────────────┐
│  Intent Classifier   │ ──► Identifies technical intent (e.g., VPN Issue, Security Incident)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Hard Constraints   │ ──► Filters out ineligible candidates (Security rules, Org policy, Partner limits)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Soft Constraints   │ ──► Scores eligible candidates (+35 Intent, +25 Asset, +10 Org, -30 Bounce Penalty)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Decision & Rationale │ ──► Selects top resolver group, calculates confidence, generates explanation
└──────────────────────┘
```

---

## 3. Technologies Used

- **Language**: Python 3.13
- **Data Manipulation**: Pandas, NumPy
- **Text & Machine Learning**: scikit-learn (TF-IDF Vectorization, Logistic Regression, Naive Bayes)
- **Web Interface**: Streamlit
- **Visualization**: Matplotlib
- **Data Storage**: Local CSV and JSON files (`data/`, `results/`)

---

## 4. System Components & Project Structure

```
f:/COE Project/
├── app.py                      # Interactive Streamlit Web Dashboard
├── config.py                   # Centralized configuration & soft constraint scoring weights
├── requirements.txt            # Python dependencies
├── data/
│   ├── tickets.csv             # Synthetic 500+ ticket dataset
│   ├── organizations.csv       # Customer organization policies & contract tiers
│   └── resolver_groups.csv     # Resolver group skills, permissions & capacity
├── src/
│   ├── data_generator.py       # Synthetic dataset & test case generator script
│   ├── baseline.py             # Text-only baseline classifier
│   ├── intent.py               # Text intent detection engine (TF-IDF + Logistic Regression)
│   ├── constraints.py          # Hard constraint filters & soft scoring functions
│   ├── router.py               # Main context-aware routing pipeline
│   └── evaluation.py           # Benchmark script calculating accuracy, F1, and bounce reduction
├── tests/
│   ├── test_cases.csv          # 10 Adversarial and edge test cases
│   └── test_router.py          # Automated test runner / Pytest suite
├── results/
│   ├── metrics.json            # Quantitative evaluation benchmark outputs
│   └── error_analysis.csv      # Categorized error breakdown table
├── README.md                   # Project documentation & module guide
├── LEARNING_GUIDE.md           # Beginner viva study guide & core concepts
└── DEMO_SCRIPT.md              # 3-minute presentation script
```

---

## 5. Hard vs Soft Constraints Explained

### Hard Constraints (Strict Eligibility Filters)
Candidates violating a hard constraint are strictly rejected (`is_eligible = False`):
1. **Security Authorization**: Security-sensitive tickets require `Security Team`.
2. **Organization Policy**: Customer contract restricts unapproved resolver groups.
3. **External Partner Restrictions**: Restricted role access limits candidate resolver teams.
4. **Priority Limits**: Priority levels (e.g. Critical) must match team capability limits.

### Soft Constraints (Weighted Compatibility Scoring)
Eligible candidates are ranked using configurable soft weights defined in `config.py`:
- **Intent Match**: `+35.0`
- **Asset Match**: `+25.0`
- **Org Match**: `+10.0`
- **Contract Compatibility**: `+10.0`
- **Priority Compatibility**: `+5.0`
- **Channel Compatibility**: `+5.0`
- **Previous Bounce Penalty**: `-30.0` (Penalizes teams that failed in prior attempts)

---

## 6. Installation & Quick Start Instructions

### 🚀 Option A: 1-Click Launch (Windows)
Double-click `run.bat` or run in PowerShell:
```cmd
.\run.bat
```
This automatically:
1. Installs Python dependencies
2. Generates/refreshes 550+ synthetic tickets (`data/tickets.csv`)
3. Trains baseline and context routers and runs evaluation benchmark
4. Runs adversarial test suite
5. Opens the Streamlit web app in your browser

---

### 🎲 Option B: Generate Data & Retrain Directly From Web UI
1. Launch the web application: `py -m streamlit run app.py`
2. Open the sidebar under **"🎲 Data & Training Generator"**
3. Choose the number of tickets (e.g. 500 to 2000) and click **"🔄 Generate New Data & Retrain Models"**
4. The system will automatically synthesize fresh tickets, retrain models, update benchmarks, and refresh the dashboard in 1 click!


---

## 7. Learning Guide for Beginners (Module Breakdown)

- **`config.py`**: Central hub holding all system settings, scoring weights, and file paths.
- **`src/data_generator.py`**: Creates realistic synthetic support tickets with realistic organization policies.
- **`src/baseline.py`**: Simple text-only baseline classifier using TF-IDF + Logistic Regression.
- **`src/intent.py`**: Detects technical problem categories (e.g., VPN Issue, Security Incident).
- **`src/constraints.py`**: Evaluates hard business rules and calculates soft weighted scores.
- **`src/router.py`**: Connects intent classification, hard filtering, soft scoring, confidence estimation, and natural language explanations into one transparent output.
- **`src/evaluation.py`**: Evaluates baseline vs context router on a 20% test split and exports metrics.
