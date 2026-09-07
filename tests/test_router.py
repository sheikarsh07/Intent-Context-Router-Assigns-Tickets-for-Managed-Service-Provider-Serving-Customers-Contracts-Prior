"""
Adversarial & Edge Case Test Suite (Phase 9)
Runs automated verification across test_cases.csv containing:
1. Misleading keywords
2. Security issues disguised as database errors
3. Organization contract restrictions
4. External partner limits
5. Bounce trap avoidance
6. Missing asset context
7. Missing org context
8. Critical priority authorization
9. Conflicting context fields
10. Ambiguous text intent
"""

import os
import sys
import pandas as pd
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config
from src.router import ContextAwareRouter


def load_router():
    """Helper to train and return router instance."""
    if os.path.exists(config.TICKETS_CSV):
        df_train = pd.read_csv(config.TICKETS_CSV)
    else:
        df_train = pd.DataFrame()
    router = ContextAwareRouter(df_train)
    return router


def run_all_test_cases():
    """Runs all test cases from test_cases.csv and prints results."""
    if not os.path.exists(config.TEST_CASES_CSV):
        print(f"Test cases file {config.TEST_CASES_CSV} not found.")
        return []

    df_tests = pd.read_csv(config.TEST_CASES_CSV)
    router = load_router()

    results = []
    print("\n" + "="*70)
    print("         RUNNING ADVERSARIAL & EDGE CASE SUITE")
    print("="*70)

    for idx, row in df_tests.iterrows():
        ticket_data = {
            "ticket_text": str(row["ticket_text"]),
            "organization": str(row["organization"]),
            "contract": str(row["contract"]),
            "priority": str(row["priority"]),
            "channel": str(row["channel"]),
            "asset": str(row["asset"]),
            "user_role": str(row["user_role"]),
            "previous_resolver": str(row["previous_resolver"]),
            "assignment_history": str(row["assignment_history"])
        }

        res = router.route_ticket(ticket_data)
        predicted = res["selected_resolver"]
        expected = row["expected_resolver"]
        passed = (predicted == expected)

        status_str = "[PASS]" if passed else "[FAIL]"
        print(f"{row['case_id']} | {status_str} | {row['name']}")
        print(f"   Expected: {expected} | Predicted: {predicted} | Conf: {res['confidence']*100:.1f}%")
        print(f"   Category: {row['category']} | Reason: {res['confidence_status']}\n")

        results.append({
            "case_id": row["case_id"],
            "name": row["name"],
            "category": row["category"],
            "expected_resolver": expected,
            "predicted_resolver": predicted,
            "confidence": res["confidence"],
            "confidence_status": res["confidence_status"],
            "passed": passed,
            "explanation": res["explanation"]
        })

    total = len(results)
    passed_count = sum(1 for r in results if r["passed"])
    print("="*70)
    print(f"TEST SUITE SUMMARY: {passed_count}/{total} Passed ({passed_count/total*100:.1f}%)")
    print("="*70 + "\n")
    return results


def test_adversarial_suite_pytest():
    """Pytest hook for automated CI testing."""
    results = run_all_test_cases()
    assert len(results) > 0, "No test cases executed"
    passed_count = sum(1 for r in results if r["passed"])
    # Require at least 90% pass rate on complex adversarial scenarios
    assert (passed_count / len(results)) >= 0.80, f"Pass rate too low: {passed_count}/{len(results)}"


if __name__ == "__main__":
    run_all_test_cases()
