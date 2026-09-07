"""
Streamlit Web Application (Phase 8)
Intent + Context Router for Managed-Service Ticket Assignment
Provides interactive Dashboard, Ticket Router, Assignment History, Quantitative Evaluation,
and Adversarial Test Cases tabs.
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import config
from src.baseline import BaselineRouter
from src.router import ContextAwareRouter
from src.evaluation import run_evaluation
from tests.test_router import run_all_test_cases

# Page Configuration
st.set_page_config(
    page_title="Intent Context Ticket Router",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .pass-badge {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .fail-badge {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models_and_data():
    """Loads dataset and trains routers."""
    if not os.path.exists(config.TICKETS_CSV):
        from src.data_generator import generate_organizations_csv, generate_resolver_groups_csv, generate_tickets_csv, generate_test_cases_csv
        generate_organizations_csv()
        generate_resolver_groups_csv()
        generate_tickets_csv()
        generate_test_cases_csv()

    df_tickets = pd.read_csv(config.TICKETS_CSV)
    
    # Train baseline & router
    baseline = BaselineRouter(model_type="logistic").train(df_tickets)
    router = ContextAwareRouter(df_tickets)
    
    # Load metrics if available, else run evaluation
    if not os.path.exists(config.METRICS_JSON):
        metrics = run_evaluation()
    else:
        with open(config.METRICS_JSON, "r") as f:
            metrics = json.load(f)

    return df_tickets, baseline, router, metrics


def main():
    st.markdown('<div class="main-header">🎫 Intent + Context Router for Ticket Assignment</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Academic Managed-Service Provider (MSP) Routing Prototype with Hard/Soft Constraints & Explainability</div>', unsafe_allow_html=True)

    df_tickets, baseline, router, metrics = load_models_and_data()

    # Sidebar Controls
    st.sidebar.title("⚙️ System Config")
    st.sidebar.info("Configurable Soft Constraint Weights (config.py)")
    
    # 1-Click Data Generation & Retraining in UI
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎲 Data & Training Generator")
    num_tickets = st.sidebar.number_input("Number of tickets to generate:", min_value=100, max_value=2000, value=550, step=50)
    if st.sidebar.button("🔄 Generate New Data & Retrain Models", use_container_width=True, type="primary"):
        with st.sidebar.status("Generating new synthetic dataset & retraining...", expanded=True) as status:
            from src.data_generator import generate_organizations_csv, generate_resolver_groups_csv, generate_tickets_csv, generate_test_cases_csv
            status.write("Generating customer orgs & resolver groups...")
            generate_organizations_csv()
            generate_resolver_groups_csv()
            status.write(f"Generating {num_tickets} realistic support tickets...")
            generate_tickets_csv(n_tickets=num_tickets, random_seed=np.random.randint(1, 10000))
            generate_test_cases_csv()
            status.write("Running benchmark evaluation...")
            run_evaluation()
            st.cache_resource.clear()
            status.update(label="Dataset & models retrained successfully!", state="complete")
        st.sidebar.success(f"Generated {num_tickets} new tickets and retrained models!")
        st.rerun()

    # 1-Click Document Downloads
    st.sidebar.markdown("---")
    st.sidebar.subheader("📄 Presentation & Viva Docs")
    docx_file = os.path.join(config.BASE_DIR, "COMPLETE_PROJECT_GUIDE.docx")
    pptx_file = os.path.join(config.BASE_DIR, "PROJECT_PRESENTATION.pptx")

    if os.path.exists(docx_file):
        with open(docx_file, "rb") as f_docx:
            st.sidebar.download_button(
                label="📥 Download Word Document (.docx)",
                data=f_docx,
                file_name="COMPLETE_PROJECT_GUIDE.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

    if os.path.exists(pptx_file):
        with open(pptx_file, "rb") as f_pptx:
            st.sidebar.download_button(
                label="📥 Download Presentation Deck (.pptx)",
                data=f_pptx,
                file_name="PROJECT_PRESENTATION.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )

    st.sidebar.markdown("---")
    with st.sidebar.expander("Adjust Soft Weights", expanded=False):


        w_intent = st.slider("Intent Match Weight", 10.0, 60.0, float(config.SOFT_WEIGHTS["intent_match"]))
        w_asset = st.slider("Asset Match Weight", 5.0, 30.0, float(config.SOFT_WEIGHTS["asset_match"]))
        w_org = st.slider("Org Policy Weight", 5.0, 20.0, float(config.SOFT_WEIGHTS["org_match"]))
        w_bounce = st.slider("Bounce Penalty Weight", -40.0, -5.0, float(config.SOFT_WEIGHTS["bounce_penalty"]))
        
        # Live override config dictionary
        config.SOFT_WEIGHTS["intent_match"] = w_intent
        config.SOFT_WEIGHTS["asset_match"] = w_asset
        config.SOFT_WEIGHTS["org_match"] = w_org
        config.SOFT_WEIGHTS["bounce_penalty"] = w_bounce

    # Main Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "🎯 Route Ticket",
        "🔄 Assignment History",
        "📈 Evaluation Benchmark",
        "🧪 Test Cases"
    ])

    # ---------------------------------------------------------
    # TAB 1: DASHBOARD
    # ---------------------------------------------------------
    with tab1:
        st.subheader("Performance Overview & KPI Dashboard")
        
        base_m = metrics["baseline"]
        router_m = metrics["context_router"]
        imp_m = metrics["improvements"]

        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Tickets", metrics["dataset_summary"]["total_tickets"])
        with col2:
            st.metric("Baseline Accuracy", f"{base_m['accuracy']*100:.1f}%")
        with col3:
            st.metric("Context Router Acc", f"{router_m['accuracy']*100:.1f}%", f"+{imp_m['accuracy_improvement_pct']:.1f}%")
        with col4:
            st.metric("Baseline Bounce Rate", f"{base_m['bounce_rate']*100:.1f}%")
        with col5:
            st.metric("Context Bounce Rate", f"{router_m['bounce_rate']*100:.1f}%", f"-{imp_m['bounce_reduction_pct']:.1f}%", delta_color="inverse")

        st.markdown("---")
        
        c_left, c_right = st.columns(2)
        
        with c_left:
            st.write("### Accuracy Comparison (Baseline vs Context Router)")
            fig, ax = plt.subplots(figsize=(6, 4))
            categories = ["Baseline (Text Only)", "Context-Aware Router"]
            accuracies = [base_m["accuracy"] * 100, router_m["accuracy"] * 100]
            colors = ["#94A3B8", "#2563EB"]
            bars = ax.bar(categories, accuracies, color=colors, width=0.5)
            ax.set_ylabel("Accuracy (%)")
            ax.set_ylim(0, 105)
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
            st.pyplot(fig)

        with c_right:
            st.write("### Bounce Rate Reduction (Baseline vs Context Router)")
            fig, ax = plt.subplots(figsize=(6, 4))
            bounces = [base_m["bounce_rate"] * 100, router_m["bounce_rate"] * 100]
            colors = ["#EF4444", "#10B981"]
            bars = ax.bar(categories, bounces, color=colors, width=0.5)
            ax.set_ylabel("Bounce Rate (%)")
            ax.set_ylim(0, 40)
            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f"{yval:.1f}%", ha='center', va='bottom', fontweight='bold')
            st.pyplot(fig)

    # ---------------------------------------------------------
    # TAB 2: ROUTE TICKET (Interactive Routing Engine)
    # ---------------------------------------------------------
    with tab2:
        st.subheader("Interactive Ticket Routing & Explanation")
        st.caption("Submit custom ticket details to view candidate scores, hard constraint validations, and decision reasons.")

        col_in1, col_in2 = st.columns([3, 2])
        
        with col_in1:
            sample_choice = st.selectbox(
                "Or load a pre-built sample scenario:",
                ["[Custom Input]", "VPN Disconnect Issue", "Database Performance Outage", "Laptop Boot Failure", "Ransomware Security Threat", "Cloud VM Unresponsive", "Misleading Text with Bounce History"]
            )
            
            # Default input values
            def_text = "Cannot connect to corporate VPN from home network"
            def_org = "ABC Corp"
            def_contract = "Standard Enterprise"
            def_prio = "High"
            def_chan = "Portal"
            def_asset = "VPN"
            def_role = "Employee"
            def_prev = "None"
            def_hist = "None"

            if sample_choice == "VPN Disconnect Issue":
                def_text = "VPN tunnel disconnects every 5 minutes with error 800"
                def_asset = "VPN"
                def_prev = "Application Team"
                def_hist = "Application Team"
            elif sample_choice == "Database Performance Outage":
                def_text = "Database query timing out for reporting service, connection pool full"
                def_asset = "Database Server"
                def_prio = "Critical"
            elif sample_choice == "Laptop Boot Failure":
                def_text = "Laptop screen flickering and failing to boot POST diagnostic"
                def_asset = "Laptop"
                def_prio = "Medium"
            elif sample_choice == "Ransomware Security Threat":
                def_text = "Ransomware alert popup detected on active directory workstation"
                def_asset = "Desktop"
                def_role = "Security Admin"
                def_prio = "Critical"
            elif sample_choice == "Cloud VM Unresponsive":
                def_text = "Azure Cloud VM unreachable via SSH connection after reboot script"
                def_asset = "Cloud VM"
                def_org = "Acme Technologies"
                def_contract = "Mission Critical"
            elif sample_choice == "Misleading Text with Bounce History":
                def_text = "Need help logging into ERP finance app over VPN connection"
                def_asset = "Application Server"
                def_prev = "Network Team"
                def_hist = "Network Team"

            ticket_text_in = st.text_area("Ticket Description / Text:", value=def_text, height=100)
            
            c_a, c_b = st.columns(2)
            with c_a:
                org_in = st.selectbox("Organization:", ["ABC Corp", "XYZ Ltd", "Acme Technologies", "Global Finance Inc"], index=0)
                prio_in = st.selectbox("Priority:", config.PRIORITIES, index=config.PRIORITIES.index(def_prio))
                asset_in = st.selectbox("Asset:", config.ASSETS, index=config.ASSETS.index(def_asset) if def_asset in config.ASSETS else 0)
                role_in = st.selectbox("User Role:", config.USER_ROLES, index=config.USER_ROLES.index(def_role) if def_role in config.USER_ROLES else 0)
            with c_b:
                contract_in = st.selectbox("Contract Tier:", config.CONTRACT_TYPES, index=0)
                channel_in = st.selectbox("Channel:", config.CHANNELS, index=0)
                prev_in = st.selectbox("Previous Resolver:", ["None"] + config.RESOLVER_GROUPS, index=0)
                hist_in = st.text_input("Assignment History:", value=def_hist)

            route_btn = st.button("🚀 Route Ticket", type="primary", use_container_width=True)

        with col_in2:
            if route_btn or sample_choice != "[Custom Input]":
                ticket_payload = {
                    "ticket_text": ticket_text_in,
                    "organization": org_in,
                    "contract": contract_in,
                    "priority": prio_in,
                    "channel": channel_in,
                    "asset": asset_in,
                    "user_role": role_in,
                    "previous_resolver": prev_in,
                    "assignment_history": hist_in
                }
                
                # Run Baseline
                b_res = baseline.predict(ticket_text_in)
                # Run Context Router
                r_res = router.route_ticket(ticket_payload)

                st.markdown("### 🏆 Routing Results")
                
                # Comparison Banner
                c_b1, c_b2 = st.columns(2)
                with c_b1:
                    st.warning(f"**Baseline Prediction**\n\n📌 **{b_res['predicted_resolver']}**\n(Conf: {b_res['confidence']*100:.1f}%)")
                with c_b2:
                    st.success(f"**Context Router**\n\n🎯 **{r_res['selected_resolver']}**\n({r_res['confidence_status']}: {r_res['confidence']*100:.1f}%)")

                st.markdown("#### 🔍 Explainability & Reasoning")
                st.info(r_res["explanation"])

                st.markdown("#### 📊 Candidate Score Breakdown")
                scores_df = pd.DataFrame([
                    {
                        "Resolver Group": r,
                        "Eligible?": "✅ Yes" if r_res["hard_constraints_evaluated"][r]["is_eligible"] else "❌ No",
                        "Total Score": f"{r_res['candidate_scores'][r]:.1f}",
                        "Rejection Reason": r_res["hard_constraints_evaluated"][r]["rejection_reasons"][0] if not r_res["hard_constraints_evaluated"][r]["is_eligible"] else "N/A"
                    } for r in config.RESOLVER_GROUPS
                ])
                st.dataframe(scores_df, use_container_width=True, hide_index=True)

    # ---------------------------------------------------------
    # TAB 3: ASSIGNMENT HISTORY & BOUNCE AVOIDANCE
    # ---------------------------------------------------------
    with tab3:
        st.subheader("Assignment History & Ticket Bounce Analysis")
        st.markdown("""
        **Ticket Bouncing** occurs when a ticket is repeatedly reassigned between resolver teams due to insufficient context or text-only routing.
        The Context-Aware Router tracks assignment history to penalize teams that failed in previous attempts.
        """)

        df_bounced = df_tickets[df_tickets["assignment_count"] > 1].head(10)
        
        st.write("### Sample Bounced Tickets from Dataset")
        st.dataframe(df_bounced[[
            "ticket_id", "ticket_text", "organization", "asset", "previous_resolver", "assignment_history", "correct_resolver"
        ]], use_container_width=True)

        st.markdown("---")
        st.write("### Live Bounce Avoidance Simulation")
        
        test_hist_ticket = {
            "ticket_text": "VPN tunnel keeps disconnecting after 5 minutes",
            "organization": "ABC Corp",
            "contract": "Standard Enterprise",
            "priority": "High",
            "channel": "Phone",
            "asset": "VPN",
            "user_role": "Manager",
            "previous_resolver": "Application Team",
            "assignment_history": "Application Team -> Hardware Team"
        }
        
        st.json(test_hist_ticket)
        res_hist = router.route_ticket(test_hist_ticket)
        
        st.success(f"**Context Router Output**: Recommended `{res_hist['selected_resolver']}` (Bounce Avoided: `{res_hist['bounce_avoided']}`)")
        st.write(res_hist["explanation"])

    # ---------------------------------------------------------
    # TAB 4: EVALUATION BENCHMARK
    # ---------------------------------------------------------
    with tab4:
        st.subheader("Quantitative System Benchmark & Error Analysis")

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.write("### Baseline vs Context-Aware Metrics")
            metrics_df = pd.DataFrame([
                {
                    "Metric": "First-Assignment Accuracy",
                    "Baseline": f"{metrics['baseline']['accuracy']*100:.2f}%",
                    "Context Router": f"{metrics['context_router']['accuracy']*100:.2f}%",
                    "Improvement": f"+{metrics['improvements']['accuracy_improvement_pct']:.2f}%"
                },
                {
                    "Metric": "Weighted Precision",
                    "Baseline": f"{metrics['baseline']['precision_weighted']*100:.2f}%",
                    "Context Router": f"{metrics['context_router']['precision_weighted']*100:.2f}%",
                    "Improvement": "N/A"
                },
                {
                    "Metric": "Weighted Recall",
                    "Baseline": f"{metrics['baseline']['recall_weighted']*100:.2f}%",
                    "Context Router": f"{metrics['context_router']['recall_weighted']*100:.2f}%",
                    "Improvement": "N/A"
                },
                {
                    "Metric": "Weighted F1 Score",
                    "Baseline": f"{metrics['baseline']['f1_weighted']*100:.2f}%",
                    "Context Router": f"{metrics['context_router']['f1_weighted']*100:.2f}%",
                    "Improvement": "N/A"
                },
                {
                    "Metric": "Bounce Rate",
                    "Baseline": f"{metrics['baseline']['bounce_rate']*100:.2f}%",
                    "Context Router": f"{metrics['context_router']['bounce_rate']*100:.2f}%",
                    "Improvement": f"-{metrics['improvements']['bounce_reduction_pct']:.2f}%"
                }
            ])
            st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        with col_m2:
            st.write("### Error Analysis Table")
            if os.path.exists(config.ERROR_ANALYSIS_CSV):
                df_errors = pd.read_csv(config.ERROR_ANALYSIS_CSV)
                st.dataframe(df_errors, use_container_width=True, height=250)
            else:
                st.info("Run evaluation script to generate error analysis table.")

    # ---------------------------------------------------------
    # TAB 5: TEST CASES
    # ---------------------------------------------------------
    with tab5:
        st.subheader("Adversarial & Edge Case Verification Suite")
        st.caption("Executes 10 complex scenarios including misleading keywords, security threats, missing context, and partner restrictions.")

        if st.button("🧪 Run Test Suite Now"):
            test_results = run_all_test_cases()
            df_test_res = pd.DataFrame(test_results)
            
            passed_c = sum(1 for r in test_results if r["passed"])
            st.success(f"Test Suite Execution Complete: **{passed_c}/{len(test_results)} Passed** ({passed_c/len(test_results)*100:.1f}%)")
            
            st.dataframe(df_test_res[[
                "case_id", "name", "category", "expected_resolver", "predicted_resolver", "passed", "confidence_status"
            ]], use_container_width=True)

            with st.expander("Detailed Test Case Explanations"):
                for tr in test_results:
                    badge = "✅ PASS" if tr["passed"] else "❌ FAIL"
                    st.markdown(f"**{tr['case_id']} - {tr['name']}** ({badge})")
                    st.write(f"Category: {tr['category']} | Expected: `{tr['expected_resolver']}` | Predicted: `{tr['predicted_resolver']}`")
                    st.text(tr["explanation"])
                    st.markdown("---")


if __name__ == "__main__":
    main()
