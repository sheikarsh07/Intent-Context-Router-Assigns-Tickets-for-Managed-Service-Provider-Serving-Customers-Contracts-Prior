"""
Evaluation Engine (Phase 7)
Evaluates Baseline vs Context-Aware Router.
Calculates:
- First-Assignment Accuracy
- Precision, Recall, F1 Score
- Bounce Rate & Bounce Reduction
- Accuracy Improvement %
- Saves results/metrics.json and results/error_analysis.csv
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config
from src.baseline import BaselineRouter
from src.router import ContextAwareRouter


def categorize_error(row, pred_baseline, pred_router):
    """Categorizes routing errors for qualitative error analysis."""
    correct = row["correct_resolver"]
    intent = row["intent"]
    text = row["ticket_text"].lower()
    asset = row["asset"]
    org = row["organization"]
    
    if pred_router == correct:
        return None  # No error

    if "vpn" in text and asset != "VPN":
        return {
            "error_type": "misleading text",
            "reason": f"Text mentions VPN keyword, but asset is {asset}.",
            "possible_improvement": "Increase asset match soft constraint weight relative to text intent."
        }
    elif intent in ["Security Incident"] and pred_router != "Security Team":
        return {
            "error_type": "insufficient permissions",
            "reason": "Security threat keyword not flagged cleanly by intent classifier.",
            "possible_improvement": "Expand security keyword lexicon in intent detection."
        }
    elif asset == "Unknown" or org == "Unknown":
        return {
            "error_type": "missing context",
            "reason": "Ticket missing asset or organization metadata.",
            "possible_improvement": "Implement automated metadata extraction from ticket body."
        }
    elif org in ["XYZ Ltd", "Global Finance Inc"]:
        return {
            "error_type": "conflicting context",
            "reason": f"Organization {org} contract restrictions conflict with natural intent resolver.",
            "possible_improvement": "Fine-tune customer contract override policy rules."
        }
    else:
        return {
            "error_type": "ambiguous intent",
            "reason": f"Ticket text '{row['ticket_text'][:50]}...' was ambiguous between teams.",
            "possible_improvement": "Prompt user for clarifying questions during ticket submission."
        }


def run_evaluation():
    """Runs end-to-end quantitative evaluation and builds metrics.json & error_analysis.csv."""
    os.makedirs(config.RESULTS_DIR, exist_ok=True)

    if not os.path.exists(config.TICKETS_CSV):
        print(f"Error: Dataset {config.TICKETS_CSV} not found. Run src/data_generator.py first.")
        return

    df_tickets = pd.read_csv(config.TICKETS_CSV)
    
    # Train / Test split (80% train, 20% test)
    train_df, test_df = train_test_split(df_tickets, test_size=0.20, random_state=42, stratify=df_tickets["correct_resolver"])

    # 1. Train Baseline
    baseline = BaselineRouter(model_type="logistic")
    baseline.train(train_df)

    # 2. Train Context-Aware Router
    context_router = ContextAwareRouter()
    context_router.train(train_df)

    # 3. Predict on Test Set
    baseline_preds = baseline.predict_dataframe(test_df)
    router_preds = context_router.route_dataframe(test_df)
    y_true = test_df["correct_resolver"].tolist()

    # 4. Compute Metrics
    # Baseline Metrics
    base_acc = accuracy_score(y_true, baseline_preds)
    base_prec, base_rec, base_f1, _ = precision_recall_fscore_support(y_true, baseline_preds, average="weighted", zero_division=0)
    base_bounce_rate = 1.0 - base_acc

    # Context Router Metrics
    router_acc = accuracy_score(y_true, router_preds)
    router_prec, router_rec, router_f1, _ = precision_recall_fscore_support(y_true, router_preds, average="weighted", zero_division=0)
    router_bounce_rate = 1.0 - router_acc

    # Improvement Calculations
    acc_improvement_pct = ((router_acc - base_acc) / base_acc) * 100.0 if base_acc > 0 else 0.0
    bounce_reduction_pct = ((base_bounce_rate - router_bounce_rate) / base_bounce_rate) * 100.0 if base_bounce_rate > 0 else 0.0

    # Class-wise metrics
    classes = sorted(list(set(y_true)))
    base_p_cls, base_r_cls, base_f1_cls, _ = precision_recall_fscore_support(y_true, baseline_preds, labels=classes, average=None, zero_division=0)
    router_p_cls, router_r_cls, router_f1_cls, _ = precision_recall_fscore_support(y_true, router_preds, labels=classes, average=None, zero_division=0)

    per_class_metrics = {}
    for i, cls_name in enumerate(classes):
        per_class_metrics[cls_name] = {
            "baseline": {
                "precision": float(base_p_cls[i]),
                "recall": float(base_r_cls[i]),
                "f1_score": float(base_f1_cls[i])
            },
            "context_router": {
                "precision": float(router_p_cls[i]),
                "recall": float(router_r_cls[i]),
                "f1_score": float(router_f1_cls[i])
            }
        }

    # Build Confusion Matrices
    cm_baseline = confusion_matrix(y_true, baseline_preds, labels=classes).tolist()
    cm_router = confusion_matrix(y_true, router_preds, labels=classes).tolist()

    metrics_result = {
        "dataset_summary": {
            "total_tickets": len(df_tickets),
            "train_size": len(train_df),
            "test_size": len(test_df)
        },
        "baseline": {
            "accuracy": float(base_acc),
            "precision_weighted": float(base_prec),
            "recall_weighted": float(base_rec),
            "f1_weighted": float(base_f1),
            "bounce_rate": float(base_bounce_rate)
        },
        "context_router": {
            "accuracy": float(router_acc),
            "precision_weighted": float(router_prec),
            "recall_weighted": float(router_rec),
            "f1_weighted": float(router_f1),
            "bounce_rate": float(router_bounce_rate)
        },
        "improvements": {
            "accuracy_improvement_pct": float(acc_improvement_pct),
            "bounce_reduction_pct": float(bounce_reduction_pct)
        },
        "labels": classes,
        "per_class_metrics": per_class_metrics,
        "confusion_matrix": {
            "baseline": cm_baseline,
            "context_router": cm_router
        }
    }

    # Save metrics.json
    with open(config.METRICS_JSON, "w") as f:
        json.dump(metrics_result, f, indent=4)
    print(f"Saved evaluation metrics to {config.METRICS_JSON}")

    # 5. Build Error Analysis Table
    error_rows = []
    test_df_reset = test_df.reset_index(drop=True)
    for idx, row in test_df_reset.iterrows():
        b_pred = baseline_preds[idx]
        r_pred = router_preds[idx]
        correct = row["correct_resolver"]

        err_info = categorize_error(row, b_pred, r_pred)
        if err_info is not None:
            error_rows.append({
                "ticket_id": row["ticket_id"],
                "organization": row["organization"],
                "asset": row["asset"],
                "actual_resolver": correct,
                "predicted_resolver": r_pred,
                "baseline_predicted": b_pred,
                "error_type": err_info["error_type"],
                "reason": err_info["reason"],
                "possible_improvement": err_info["possible_improvement"]
            })

    df_errors = pd.DataFrame(error_rows)
    if df_errors.empty:
        # Dummy placeholder row if 0 errors
        df_errors = pd.DataFrame([{
            "ticket_id": "NONE",
            "organization": "N/A",
            "asset": "N/A",
            "actual_resolver": "N/A",
            "predicted_resolver": "N/A",
            "baseline_predicted": "N/A",
            "error_type": "none",
            "reason": "100% accuracy achieved on test set",
            "possible_improvement": "Maintain current weights"
        }])

    df_errors.to_csv(config.ERROR_ANALYSIS_CSV, index=False)
    print(f"Saved {len(df_errors)} error analysis records to {config.ERROR_ANALYSIS_CSV}")

    # Print summary report to console
    print("\n" + "="*50)
    print("      EVALUATION BENCHMARK SUMMARY REPORT")
    print("="*50)
    print(f"Baseline Accuracy       : {base_acc*100:.2f}% | Bounce Rate: {base_bounce_rate*100:.2f}%")
    print(f"Context-Router Accuracy: {router_acc*100:.2f}% | Bounce Rate: {router_bounce_rate*100:.2f}%")
    print(f"Accuracy Improvement    : +{acc_improvement_pct:.2f}%")
    print(f"Bounce Rate Reduction  : -{bounce_reduction_pct:.2f}%")
    print("="*50 + "\n")

    return metrics_result


if __name__ == "__main__":
    run_evaluation()
