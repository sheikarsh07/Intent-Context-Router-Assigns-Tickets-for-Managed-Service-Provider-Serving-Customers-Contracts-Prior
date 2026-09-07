# Viva Study Guide: Intent + Context Router

> **Welcome!** This guide explains all key computer science, data analytics, and machine learning concepts used in this project in plain, beginner-friendly language to help you excel in your project viva examination.

---

## 1. Core Technical Concepts

### 1. Natural Language Processing (NLP)
* **What it is**: NLP is a branch of Artificial Intelligence (AI) that helps computers understand, interpret, and process human text language.
* **In this project**: We use NLP to take a raw support ticket description written by a user (e.g., *"My laptop screen is flickering and won't turn on"*) and analyze the text to extract the technical problem.

### 2. TF-IDF (Term Frequency - Inverse Document Frequency)
* **What it is**: A mathematical technique that converts text words into numerical numbers that machine learning algorithms can understand.
  * **Term Frequency (TF)**: Counts how often a word appears in a specific ticket.
  * **Inverse Document Frequency (IDF)**: Gives less weight to common words like *"the"*, *"is"*, *"a"*, and gives higher weight to rare technical words like *"ransomware"*, *"VPN"*, *"SQL"*.
* **In this project**: We use `TfidfVectorizer` from `scikit-learn` to convert ticket descriptions into numbers for text classification.

### 3. Intent Classification
* **What it is**: Categorizing a piece of text into predefined goal categories (intents).
* **In this project**: The intent classifier maps ticket text to technical intent categories: `VPN Issue`, `Database Outage`, `Hardware Fault`, `Security Incident`, `Application Crash`, `Cloud Outage`.

### 4. Baseline System
* **What it is**: A simple standard method used as a benchmark to compare against our new system.
* **In this project**: Our baseline is a text-only classifier (`BaselineRouter`). It routes tickets based *only* on ticket description text without looking at organization, contract, asset, user role, or history.

### 5. Hard Constraints vs Soft Constraints
* **Hard Constraints**: Strict binary rules (YES / NO). If a candidate resolver violates a hard constraint, it is strictly **rejected** and eliminated.
  * *Example*: A security incident strictly requires `Security Team`. An unapproved resolver team for a customer contract is strictly rejected.
* **Soft Constraints**: Configurable scoring preferences that assign points (+ / -) to eligible teams based on context matches.
  * *Example*: `+35` for intent match, `+25` for asset match, `+10` for org policy match, `-30` bounce penalty for previously failed teams.

### 6. Weighted Scoring Algorithm
* **What it is**: A mathematical formula where different factors are multiplied by weights representing their importance.
  $$\text{Total Score} = w_{\text{intent}} \cdot S_{\text{intent}} + w_{\text{asset}} \cdot S_{\text{asset}} + w_{\text{org}} \cdot S_{\text{org}} - \text{Bounce Penalty}$$
* **In this project**: We combine soft scores for each eligible team and select the highest-scoring candidate.

### 7. Ticket Bouncing & Bounce Rate
* **What it is**: **Ticket Bouncing** occurs when a support ticket is assigned to the wrong resolver group and must be reassigned multiple times.
* **Bounce Rate Formula**:
  $$\text{Bounce Rate} = \frac{\text{Number of Bounced Tickets}}{\text{Total Tickets}} = 1.0 - \text{First Assignment Accuracy}$$
* **In this project**: Our context router reduces ticket bouncing by penalizing previously failed resolver teams.

### 8. Evaluation Metrics
* **First-Assignment Accuracy**: Percentage of tickets correctly routed on the first attempt.
* **Precision**: Out of all tickets predicted for Team A, how many were actually for Team A?
* **Recall**: Out of all actual tickets for Team A, how many did the system find?
* **F1 Score**: The harmonic mean of Precision and Recall ($2 \times \frac{P \times R}{P + R}$).

---

## 2. Top Viva Questions & Answers

### Q1: Why did you build a context-aware router instead of relying only on NLP text classification?
> **Answer**: Text alone is ambiguous and lacks operational awareness. For example, a ticket saying *"ERP app crashing over VPN"* contains the keyword "VPN", causing text-only models to misassign it to Network Team. Context-aware routing incorporates asset metadata (`Application Server`), contract restrictions, and past assignment history to select the correct team and avoid ticket bouncing.

### Q2: What is the difference between Hard Constraints and Soft Constraints in your project?
> **Answer**: Hard constraints are strict binary filters (e.g. security permissions, organization contract limits). If a resolver team violates a hard constraint, it is strictly eliminated. Soft constraints are weighted scoring criteria (e.g. intent match +35, asset match +25, bounce penalty -30) used to rank remaining eligible teams.

### Q3: How does your system prevent repeated ticket bouncing?
> **Answer**: Our router tracks assignment history. If a ticket was previously assigned to a team that failed to resolve it, that team incurs a **Bounce Penalty (-30)** in the soft scoring phase, preventing the system from assigning the ticket back to the same wrong team.

### Q4: How is your system explainable?
> **Answer**: Instead of using a black-box model, every routing decision produces a transparent breakdown showing: (1) which hard constraints were evaluated, (2) exact soft score contributions (+35 intent, +25 asset, etc.), (3) rejected candidates with exact policy reasons, and (4) confidence status.

### Q5: What results did you achieve when comparing your router against the baseline?
> **Answer**: The proposed context-aware router improved First-Assignment Accuracy from **85.45% (baseline)** to **90.00% (context router)**, and reduced the ticket bounce rate by **31.25%** on the test dataset.
