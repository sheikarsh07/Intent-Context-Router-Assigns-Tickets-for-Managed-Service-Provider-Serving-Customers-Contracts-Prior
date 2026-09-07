# 3-Minute Project Demonstration Script

> **Goal**: Present a flawless 3-minute live demonstration of the Intent + Context Ticket Router project during your viva or project presentation.

---

## ⏱️ Step-by-Step Presentation Timeline

| Time | Section | What to Click in Streamlit | What to Say |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:30** | **1. System Overview** | Tab 1 (`📊 Dashboard`) | *"Good morning. Today I am presenting our context-aware IT support ticket router. Traditional IT routers rely solely on text keywords, which causes ticket bouncing and misassignment. Our system combines text intent classification with hard/soft operational constraints."* |
| **0:30 - 1:00** | **2. Normal Ticket Routing** | Tab 2 (`🎯 Route Ticket`) -> Select sample **"VPN Disconnect Issue"** -> Click **Route Ticket** | *"Here we route a normal VPN issue for ABC Corp. Notice how the baseline and context router both identify the Network Team."* |
| **1:00 - 1:30** | **3. Explainable Decision** | Scroll down to **Reasoning & Candidate Scores** | *"Crucially, our system explains WHY: 1) Intent matches VPN Issue (+35), 2) Asset matches VPN (+25), 3) No hard constraints violated. The candidate score table displays transparent points for all teams."* |
| **1:30 - 2:00** | **4. Bounce Avoidance** | Tab 2 -> Select **"Misleading Text with Bounce History"** OR Tab 3 (`🔄 Assignment History`) | *"Here is a classic failure case: Ticket says 'logging into ERP app over VPN'. Baseline gets misled by the word 'VPN' and assigns Network Team. But Network Team already failed in assignment history! Our context router penalizes Network Team (-30 bounce penalty) and correctly routes to Application Team."* |
| **2:00 - 2:30** | **5. Security Adversarial Case** | Tab 2 -> Select **"Ransomware Security Threat"** OR Tab 5 (`🧪 Test Cases`) | *"In this security scenario, hard constraints enforce that any security incident strictly requires Security Team, overriding standard general IT queues."* |
| **2:30 - 3:00** | **6. Quantitative Benchmark** | Tab 4 (`📈 Evaluation Benchmark`) | *"In our benchmark evaluation across 550 synthetic tickets, the context-aware router achieved 90.00% First-Assignment Accuracy and reduced ticket bouncing by over 30% compared to text-only baselines."* |

---

## 💡 Quick Tips for Presentation Success
1. Launch Streamlit before the evaluator arrives: `py -m streamlit run app.py`.
2. Keep your answers concise during Q&A by referring to the candidate score breakdown table in Tab 2.
