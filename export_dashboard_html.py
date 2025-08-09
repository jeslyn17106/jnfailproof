import pandas as pd
import ast
import plotly.express as px
import os

# Load data
df = pd.read_csv('results/stress_results.csv')

def classify_failure(row):
    import re

    def looks_nonsense(text):
        if not text or not isinstance(text, str):
            return True
        text = text.strip().lower()
        if len(text) < 10:
            return True
        alnum_chars = len(re.findall(r'[a-z0-9]', text))
        ratio = alnum_chars / max(len(text), 1)
        if ratio < 0.5:
            return True
        words = re.findall(r'\b\w+\b', text)
        if words:
            most_common = max(set(words), key=words.count)
            if words.count(most_common) > 5:
                return True
        return False

    error = str(row.get('error', '')).strip()
    if error != '':
        lowered_error = error.lower()
        if any(k in lowered_error for k in ['error', 'exception', 'crash', 'fail']):
            return 'Crash/Error'
        if 'policy' in lowered_error:
            return 'Policy Violation'
    try:
        response_obj = ast.literal_eval(row['response'])
    except Exception:
        return 'Incorrect Output'

    if isinstance(response_obj, list) and len(response_obj) > 0 and isinstance(response_obj[0], dict):
        combined_text = ' '.join(str(v) for d in response_obj for v in d.values()).lower()
    else:
        combined_text = str(response_obj).lower()

    refusal_keywords = ['refuse', 'cannot', 'deny', 'no comment', 'decline']
    if any(word in combined_text for word in refusal_keywords):
        return 'Refusal'
    if 'policy' in combined_text:
        return 'Policy Violation'
    if looks_nonsense(combined_text):
        return 'Incorrect Output'
    return 'Success'

df['failure_type'] = df.apply(classify_failure, axis=1)

failure_counts = df['failure_type'].value_counts().reset_index()
failure_counts.columns = ['Failure Type', 'Count']

fig_pie = px.pie(failure_counts, names='Failure Type', values='Count',
                 title='Failure Types Distribution',
                 color_discrete_sequence=px.colors.qualitative.Pastel)

fig_bar = px.bar(failure_counts, x='Failure Type', y='Count',
                 title='Failure Counts',
                 color='Failure Type',
                 color_discrete_sequence=px.colors.qualitative.Pastel)

# Make sure reports folder exists
os.makedirs('reports', exist_ok=True)

# Save figures as standalone HTML files
fig_pie.write_html('reports/failure_pie_chart.html')
fig_bar.write_html('reports/failure_bar_chart.html')

print("Charts saved as HTML files in the 'reports' folder.")
