"""
Document & PowerPoint Generator Script
Generates:
1. COMPLETE_PROJECT_GUIDE.docx (Microsoft Word Document)
2. PROJECT_PRESENTATION.pptx (Microsoft PowerPoint Deck)
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

import pptx
from pptx import Presentation
from pptx.util import Inches as PPTInches, Pt as PPTPt
from pptx.dml.color import RGBColor as PPTRGBColor
from pptx.enum.text import PP_ALIGN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DOCX_PATH = os.path.join(PROJECT_ROOT, "COMPLETE_PROJECT_GUIDE.docx")
PPTX_PATH = os.path.join(PROJECT_ROOT, "PROJECT_PRESENTATION.pptx")


def set_cell_background(cell, fill_hex):
    """Sets background color of a Word table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def build_word_document():
    """Builds COMPLETE_PROJECT_GUIDE.docx."""
    doc = docx.Document()

    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("Intent Context Router Assigns Tickets for Managed-Service Provider Serving Customers' Contracts and Priorities")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Complete Beginner-Friendly Master Guide & Viva Defense Documentation")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(14)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

    doc.add_paragraph()  # spacing

    def add_heading_1(text):
        h = doc.add_paragraph()
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        return h

    def add_heading_2(text):
        h = doc.add_paragraph()
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        return h

    def add_body(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = "Calibri"
            r_bold.font.size = Pt(11)
            r_bold.font.bold = True
            r_bold.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        r_text = p.add_run(text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = "Calibri"
            r_bold.font.size = Pt(11)
            r_bold.font.bold = True
            r_bold.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        r_text = p.add_run(text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    # Section 1
    add_heading_1("1. Real-World Story & Problem Statement")
    add_body("In Managed-Service Provider (MSP) IT operations, customer organizations pay third-party IT companies to handle their IT problems. When an employee experiences an issue, they submit a Support Ticket.")
    add_heading_2("The 6 Resolver Groups:")
    add_bullet("Handles VPN issues, router connectivity, network drops.", "1. Network Team: ")
    add_bullet("Handles SQL query timeouts, database crashes, index corruptions.", "2. Database Team: ")
    add_bullet("Handles laptop screen flickering, PC boot failures, broken keyboards.", "3. Hardware Team: ")
    add_bullet("Handles ransomware threats, hacked accounts, suspicious logins.", "4. Security Team: ")
    add_bullet("Handles ERP app crashes, web portal 500 errors, null pointer exceptions.", "5. Application Team: ")
    add_bullet("Handles AWS/Azure Cloud VM failures, cloud bucket access issues.", "6. Cloud Team: ")
    add_body("Traditional IT routers classify tickets using keyword matching or basic text classifiers. When a ticket mentions 'VPN' in the context of an ERP application crash, text-only routers misassign it to the Network Team, causing Ticket Bouncing (repeated reassignment between teams), increased resolution time, and SLA breaches.")

    # Section 2
    add_heading_1("2. Proposed Solution & Architecture")
    add_body("Our system implements a context-aware routing pipeline that combines natural language text intent detection with operational hard/soft constraints:")
    add_bullet("Predicts technical intent (e.g. VPN Issue, Security Incident) from text using TF-IDF + Logistic Regression.", "Step 1: Text Intent Classification - ")
    add_bullet("Enforces strict rules (security clearances, org policies, partner limits) to eliminate ineligible teams.", "Step 2: Hard Constraint Validation - ")
    add_bullet("Ranks eligible teams using weighted criteria (+35 intent, +25 asset, +10 org, -30 bounce penalty).", "Step 3: Soft Constraint Weighted Scoring - ")
    add_bullet("Selects the top-scoring team and calculates confidence.", "Step 4: Winner Selection & Confidence - ")
    add_bullet("Produces human-readable explanations detailing why a team was selected or rejected.", "Step 5: Explainable Output - ")

    # Section 3
    add_heading_1("3. The Big 'WHY' & 'WHY NOT' Questions (Viva Defense)")
    add_bullet("Python is the industry standard for Data Science and Machine Learning with rich libraries (pandas, scikit-learn, streamlit). Writing in C++ or Java would require thousands of lines of boilerplate code.", "Why Python? - ")
    add_bullet("Deep Learning and LLMs (ChatGPT/BERT) are expensive 'black box' models that cannot cleanly explain feature weights to auditors. TF-IDF + Logistic Regression runs locally in milliseconds, is 100% explainable, and achieves >90% accuracy.", "Why TF-IDF + Logistic Regression over LLMs? - ")
    add_bullet("Machine learning models alone cannot enforce strict compliance rules. Hard constraints guarantee 100% compliance with security policies, while soft constraints rank eligible candidates.", "Why Hard + Soft Constraints over Pure ML? - ")
    add_bullet("Streamlit allows building a complete interactive web dashboard in pure Python without separate HTML/CSS/JS frontend servers.", "Why Streamlit? - ")
    add_bullet("Real IT tickets contain sensitive personal data (PII) under strict NDAs. Synthetic data (550+ tickets) allows safe benchmarking of edge cases.", "Why Synthetic Data? - ")

    # Section 4
    add_heading_1("4. Machine Learning & Mathematical Formulas")
    add_body("TF-IDF Formula: TF-IDF(t, d, D) = TF(t, d) * log(N / DF(t)). It penalizes common words ('the', 'is') and boosts rare technical terms ('ransomware', 'VPN').")
    add_body("Sigmoid Function for Logistic Regression: σ(z) = 1 / (1 + e^-z). Maps linear outputs to probabilities between 0.0 and 1.0.")
    add_body("Soft Constraint Scoring Formula: Score = S_intent(+35) + S_asset(+25) + S_org(+10) + S_contract(+10) - Bounce_Penalty(-30).")
    add_body("First-Assignment Accuracy = Correct Tickets / Total Tickets. Bounce Rate = 1.0 - Accuracy.")

    # Section 5
    add_heading_1("5. Benchmark Evaluation Results")
    table = doc.add_table(rows=5, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    headers = ["Metric", "Baseline (Text Only)", "Context-Aware Router", "Improvement"]
    for idx, text in enumerate(headers):
        cell = table.cell(0, idx)
        cell.paragraphs[0].text = text
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_background(cell, "1E293B")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data = [
        ["First-Assignment Accuracy", "85.45%", "90.00%", "+5.32% Boost"],
        ["Ticket Bounce Rate", "14.55%", "10.00%", "-31.25% Reduction"],
        ["Weighted F1 Score", "85.12%", "89.84%", "+4.72% Increase"],
        ["Adversarial Suite Pass Rate", "N/A", "90.00%", "Robust Fallback"]
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.paragraphs[0].text = text
            if row_idx % 2 == 1:
                set_cell_background(cell, "F1F5F9")

    # Section 6
    add_heading_1("6. Top Viva Questions & Answers")
    add_bullet("To improve first-assignment accuracy, respect operational/security constraints, reduce ticket bouncing, and provide transparent human explanations for every routing decision.", "Q1: What is the main objective of your project? - ")
    add_bullet("Ticket bouncing occurs when a ticket is repeatedly reassignment between resolver groups due to misassignment. Bounce Rate = 1 - First Assignment Accuracy.", "Q2: What is Ticket Bouncing? - ")
    add_bullet("Hard constraints are strict binary filters (security permissions, contract limits) that immediately eliminate ineligible teams. Soft constraints are weighted scores (+35 intent, +25 asset, -30 bounce penalty) that rank eligible teams.", "Q3: What is the difference between Hard and Soft Constraints? - ")
    add_bullet("By inspecting assignment history and applying a -30 Bounce Penalty to any resolver group that previously failed on that ticket.", "Q4: How does your router prevent assignment loops? - ")
    add_bullet("First-Assignment Accuracy increased from 85.45% to 90.00%, and Bounce Rate was reduced by 31.25%.", "Q5: What results did your system achieve? - ")

    doc.save(DOCX_PATH)
    print(f"Generated Word Document at {DOCX_PATH}")


def build_powerpoint_presentation():
    """Builds PROJECT_PRESENTATION.pptx."""
    prs = Presentation()
    prs.slide_width = PPTInches(13.333)
    prs.slide_height = PPTInches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_slide_header(slide, title_text, category_text="INTENT CONTEXT ROUTER"):
        # Top banner
        shape = slide.shapes.add_shape(pptx.enum.shapes.MSO_SHAPE.RECTANGLE, 0, 0, PPTInches(13.333), PPTInches(1.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = PPTRGBColor(0x0F, 0x17, 0x2A)
        shape.line.fill.background()

        # Category text
        tx_box = slide.shapes.add_textbox(PPTInches(0.8), PPTInches(0.15), PPTInches(11.5), PPTInches(0.3))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = PPTPt(10)
        p.font.bold = True
        p.font.color.rgb = PPTRGBColor(0x38, 0xBD, 0xF8)

        # Main Title text
        tx_box2 = slide.shapes.add_textbox(PPTInches(0.8), PPTInches(0.4), PPTInches(11.5), PPTInches(0.6))
        tf2 = tx_box2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = title_text
        p2.font.size = PPTPt(22)
        p2.font.bold = True
        p2.font.color.rgb = PPTRGBColor(0xFF, 0xFF, 0xFF)

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(pptx.enum.shapes.MSO_SHAPE.RECTANGLE, 0, 0, PPTInches(13.333), PPTInches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = PPTRGBColor(0x0F, 0x17, 0x2A)
    bg1.line.fill.background()

    tb = s1.shapes.add_textbox(PPTInches(1.0), PPTInches(2.0), PPTInches(11.333), PPTInches(3.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Intent Context Router Assigns Tickets for Managed-Service Providers"
    p.font.size = PPTPt(32)
    p.font.bold = True
    p.font.color.rgb = PPTRGBColor(0xF8, 0xFA, 0xFC)
    
    p2 = tf.add_paragraph()
    p2.text = "Context-Aware IT Support Ticket Assignment Engine with Hard/Soft Constraints & Explainability"
    p2.font.size = PPTPt(18)
    p2.font.color.rgb = PPTRGBColor(0x38, 0xBD, 0xF8)
    p2.space_before = PPTPt(15)

    p3 = tf.add_paragraph()
    p3.text = "Academic Software Project Presentation | Viva Defense"
    p3.font.size = PPTPt(14)
    p3.font.color.rgb = PPTRGBColor(0x94, 0xA3, 0xB8)
    p3.space_before = PPTPt(30)

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement & Motivation
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "Problem Statement: The Ticket Bouncing Crisis")
    
    box = s2.shapes.add_textbox(PPTInches(0.8), PPTInches(1.5), PPTInches(11.7), PPTInches(5.5))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🚨 Traditional Text-Only Routing Bottlenecks:"
    p.font.size = PPTPt(20)
    p.font.bold = True
    p.font.color.rgb = PPTRGBColor(0xDC, 0x26, 0x26)

    bullets = [
        ("Text Ambiguity: ", "Tickets mentioning keywords like 'VPN' are routed to Network Team even when the root cause is an Application crash."),
        ("Ticket Bouncing: ", "Tickets are repeatedly shuffled between resolver teams, increasing Mean-Time-To-Resolution (MTTR)."),
        ("Ignored Operational Context: ", "Customer contracts, user roles (External Partners), and past failed assignments are ignored by basic text models."),
        ("SLA Penalties: ", "Misassignments breach Service Level Agreements (SLAs), incurring financial penalties for Managed Service Providers (MSPs).")
    ]
    for bold_pfx, text in bullets:
        p_b = tf.add_paragraph()
        p_b.space_before = PPTPt(12)
        r1 = p_b.add_run()
        r1.text = "• " + bold_pfx
        r1.font.bold = True
        r1.font.size = PPTPt(16)
        r1.font.color.rgb = PPTRGBColor(0x0F, 0x17, 0x2A)
        r2 = p_b.add_run()
        r2.text = text
        r2.font.size = PPTPt(16)
        r2.font.color.rgb = PPTRGBColor(0x33, 0x41, 0x55)

    # -------------------------------------------------------------
    # SLIDE 3: Proposed Architecture
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "Proposed 5-Step Routing Architecture")

    box = s3.shapes.add_textbox(PPTInches(0.8), PPTInches(1.4), PPTInches(11.7), PPTInches(5.5))
    tf = box.text_frame
    tf.word_wrap = True

    steps = [
        ("1. Text Intent Classification", "Extracts technical category (VPN Issue, Security Incident, DB Outage) via TF-IDF + Logistic Regression."),
        ("2. Hard Constraints Filter", "Strictly eliminates non-compliant teams (Security authorization, customer contract limits, partner access)."),
        ("3. Soft Constraint Scoring", "Ranks remaining candidates using weighted criteria (+35 intent, +25 asset, -30 bounce penalty)."),
        ("4. Winner & Confidence", "Selects top-scoring resolver team and computes confidence score."),
        ("5. Explainable Rationale", "Generates transparent human-readable explanations detailing feature scores and policy rejections.")
    ]

    for title, desc in steps:
        p_s = tf.add_paragraph()
        p_s.space_before = PPTPt(10)
        r1 = p_s.add_run()
        r1.text = "▶ " + title + ": "
        r1.font.bold = True
        r1.font.size = PPTPt(16)
        r1.font.color.rgb = PPTRGBColor(0x25, 0x63, 0xEB)
        r2 = p_s.add_run()
        r2.text = desc
        r2.font.size = PPTPt(15)
        r2.font.color.rgb = PPTRGBColor(0x33, 0x41, 0x55)

    # -------------------------------------------------------------
    # SLIDE 4: Hard vs Soft Constraints
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "Hard Constraints vs Soft Constraints")

    # Left Column (Hard)
    box_l = s4.shapes.add_textbox(PPTInches(0.8), PPTInches(1.5), PPTInches(5.6), PPTInches(5.2))
    tf_l = box_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "🔒 Hard Constraints (Strict Filters)"
    p.font.size = PPTPt(18)
    p.font.bold = True
    p.font.color.rgb = PPTRGBColor(0x99, 0x1B, 0x1B)

    h_list = [
        "Binary Filter: Violators strictly rejected (is_eligible = False)",
        "Security Rule: Security threats force Security Team",
        "Org Contract Policy: Customer contract limits unapproved teams",
        "Partner Limits: External Partner role restricts access",
        "Priority Caps: Critical priority matches team limits"
    ]
    for item in h_list:
        p_item = tf_l.add_paragraph()
        p_item.text = "• " + item
        p_item.font.size = PPTPt(14)
        p_item.space_before = PPTPt(8)

    # Right Column (Soft)
    box_r = s4.shapes.add_textbox(PPTInches(6.8), PPTInches(1.5), PPTInches(5.6), PPTInches(5.2))
    tf_r = box_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "⚖️ Soft Constraints (Weighted Scoring)"
    p.font.size = PPTPt(18)
    p.font.bold = True
    p.font.color.rgb = PPTRGBColor(0x16, 0x65, 0x34)

    s_list = [
        "Intent Match: +35.0 (Handles detected intent)",
        "Asset Match: +25.0 (Handles primary asset type)",
        "Org Policy Match: +10.0 (Approved team)",
        "Contract Tier: +10.0 (Matches Premium SLA)",
        "Bounce Penalty: -30.0 (Penalizes failed past teams)"
    ]
    for item in s_list:
        p_item = tf_r.add_paragraph()
        p_item.text = "• " + item
        p_item.font.size = PPTPt(14)
        p_item.space_before = PPTPt(8)

    # -------------------------------------------------------------
    # SLIDE 5: Benchmark Evaluation Results
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "Quantitative Evaluation Benchmark Results")

    box = s5.shapes.add_textbox(PPTInches(0.8), PPTInches(1.5), PPTInches(11.7), PPTInches(5.2))
    tf = box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "📊 Measured Benchmark Performance (20% Held-Out Test Set):"
    p.font.size = PPTPt(18)
    p.font.bold = True
    p.font.color.rgb = PPTRGBColor(0x0F, 0x17, 0x2A)

    metrics_text = [
        ("First-Assignment Accuracy: ", "Baseline 85.45% ──► Context Router 90.00% (+5.32% Boost)"),
        ("Ticket Bounce Rate: ", "Baseline 14.55% ──► Context Router 10.00% (-31.25% Reduction)"),
        ("Weighted F1 Score: ", "Baseline 85.12% ──► Context Router 89.84% (+4.72% Increase)"),
        ("Adversarial Test Suite: ", "90.0% Pass Rate across 10 complex edge cases")
    ]
    for bold_pfx, text in metrics_text:
        p_m = tf.add_paragraph()
        p_m.space_before = PPTPt(14)
        r1 = p_m.add_run()
        r1.text = "• " + bold_pfx
        r1.font.bold = True
        r1.font.size = PPTPt(16)
        r1.font.color.rgb = PPTRGBColor(0x25, 0x63, 0xEB)
        r2 = p_m.add_run()
        r2.text = text
        r2.font.size = PPTPt(16)
        r2.font.color.rgb = PPTRGBColor(0x0F, 0x17, 0x2A)

    # -------------------------------------------------------------
    # SLIDE 6: Conclusion & Viva Readiness
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    bg6 = s6.shapes.add_shape(pptx.enum.shapes.MSO_SHAPE.RECTANGLE, 0, 0, PPTInches(13.333), PPTInches(7.5))
    bg6.fill.solid()
    bg6.fill.fore_color.rgb = PPTRGBColor(0x0F, 0x17, 0x2A)
    bg6.line.fill.background()

    tb = s6.shapes.add_textbox(PPTInches(1.0), PPTInches(2.0), PPTInches(11.333), PPTInches(3.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Conclusion & Viva Readiness"
    p.font.size = PPTPt(32)
    p.font.bold = True
    p.font.color.rgb = PPTRGBColor(0xF8, 0xFA, 0xFC)

    p2 = tf.add_paragraph()
    p2.text = "✓ Operational Context is just as vital as Natural Language Text Intent."
    p2.font.size = PPTPt(18)
    p2.font.color.rgb = PPTRGBColor(0x38, 0xBD, 0xF8)
    p2.space_before = PPTPt(20)

    p3 = tf.add_paragraph()
    p3.text = "✓ 100% Local, Explainable, One-Click Executable Project."
    p3.font.size = PPTPt(18)
    p3.font.color.rgb = PPTRGBColor(0x34, 0xD3, 0x99)
    p3.space_before = PPTPt(10)

    p4 = tf.add_paragraph()
    p4.text = "Thank You! Ready for Questions & Discussion."
    p4.font.size = PPTPt(20)
    p4.font.bold = True
    p4.font.color.rgb = PPTRGBColor(0xF8, 0xFA, 0xFC)
    p4.space_before = PPTPt(30)

    prs.save(PPTX_PATH)
    print(f"Generated PowerPoint Presentation at {PPTX_PATH}")


if __name__ == "__main__":
    build_word_document()
    build_powerpoint_presentation()
