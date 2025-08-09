import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
import os
import ast
import re

RESULTS_CSV = "results/stress_results.csv"
REPORTS_DIR = "reports"
REPORT_PDF = os.path.join(REPORTS_DIR, "failure_report.pdf")
PIE_IMG = os.path.join(REPORTS_DIR, "failure_pie.png")

# Create reports directory if needed
os.makedirs(REPORTS_DIR, exist_ok=True)

def looks_nonsense(text):
    if not text or not isinstance(text, str):
        return True  # Empty or non-string is nonsense

    text = text.strip().lower()

    # Short text is suspicious
    if len(text) < 10:
        return True

    # Check ratio of alphanumeric chars
    alnum_chars = len(re.findall(r'[a-z0-9]', text))
    ratio = alnum_chars / max(len(text), 1)
    if ratio < 0.5:
        return True

    # Check repetitive words
    words = re.findall(r'\b\w+\b', text)
    if words:
        most_common = max(set(words), key=words.count)
        if words.count(most_common) > 5:
            return True

    return False

def classify_failure(row):
    # Check errors first
    error = str(row.get('error', '')).strip()
    if error != '':
        lowered_error = error.lower()
        if any(k in lowered_error for k in ['error', 'exception', 'crash', 'fail']):
            return 'Crash/Error'
        if 'policy' in lowered_error:
            return 'Policy Violation'

    # Parse the response string safely
    try:
        response_obj = ast.literal_eval(row['response'])
    except Exception:
        # Can't parse response, treat as failure
        return 'Incorrect Output'

    # Extract text from response object
    if isinstance(response_obj, list) and len(response_obj) > 0 and isinstance(response_obj[0], dict):
        combined_text = ' '.join(str(v) for d in response_obj for v in d.values()).lower()
    else:
        combined_text = str(response_obj).lower()

    # Refusal check
    refusal_keywords = ['refuse', 'cannot', 'deny', 'no comment', 'decline']
    if any(word in combined_text for word in refusal_keywords):
        return 'Refusal'

    # Policy violation
    if 'policy' in combined_text:
        return 'Policy Violation'

    # Nonsense check
    if looks_nonsense(combined_text):
        return 'Incorrect Output'

    return 'Success'

def generate_pie_chart(df):
    failure_counts = df['failure_type'].value_counts()
    plt.figure(figsize=(6,6))
    failure_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
    plt.title("Failure Types Distribution")
    plt.ylabel('')
    plt.savefig(PIE_IMG)
    plt.close()

def generate_pdf_report(df):
    doc = SimpleDocTemplate(REPORT_PDF, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("FailProof LLM - Failure Analysis Report", styles['Title']))
    elements.append(Spacer(1, 12))

    # Add pie chart
    elements.append(Paragraph("Failure Type Distribution", styles['Heading2']))
    elements.append(Image(PIE_IMG, width=300, height=300))
    elements.append(Spacer(1, 12))

    # Summary table header
    elements.append(Paragraph("Summary of Test Cases and Failures", styles['Heading2']))

    # Create table data with headers
    table_data = [["Prompt (truncated)", "Latency (s)", "Failure Type"]]

    # Limit to first 20 entries for brevity
    for _, row in df.head(20).iterrows():
        prompt_trunc = (row['prompt'][:50] + "...") if len(row['prompt']) > 50 else row['prompt']
        latency = f"{row['latency_sec']:.3f}"
        failure = row['failure_type']
        table_data.append([prompt_trunc, latency, failure])

    # Create and style table
    table = Table(table_data, colWidths=[300, 60, 100])
    elements.append(table)

    doc.build(elements)
    print(f"PDF report generated at {REPORT_PDF}")

def main():
    # Load CSV
    if not os.path.exists(RESULTS_CSV):
        print(f"❌ Results file not found: {RESULTS_CSV}")
        return

    df = pd.read_csv(RESULTS_CSV)

    # Fill missing latency_sec with 0 if any
    df['latency_sec'] = df.get('latency_sec', 0).fillna(0)

    # Classify failures
    df['failure_type'] = df.apply(classify_failure, axis=1)

    # Generate pie chart image
    generate_pie_chart(df)

    # Generate PDF report
    generate_pdf_report(df)

    print("✅ Failure analysis complete.")

if __name__ == "__main__":
    main()
