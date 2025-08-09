import pandas as pd
import ast
import re
import os
import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data
df = pd.read_csv('results/stress_results.csv')

# Failure classification function (more general)
def classify_failure(row):
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
    if error:
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

# Count failure types
failure_counts = df['failure_type'].value_counts()

# Prepare test case details for table (show prompt, failure_type, latency, error)
table_df = df[['prompt', 'failure_type', 'latency_sec', 'error']].copy()
table_df.rename(columns={
    'prompt': 'Test Case',
    'failure_type': 'Failure Type',
    'latency_sec': 'Latency (s)',
    'error': 'Error'
}, inplace=True)

# Create subplot figure: 2 rows, 2 cols (pie + bar + table)
fig = make_subplots(
    rows=3, cols=1,
    specs=[[{"type": "domain"}],
           [{"type": "bar"}],
           [{"type": "table"}]],
    subplot_titles=("Failure Types Distribution", "Failure Counts", "Test Case Details")
)

# Pie chart
fig.add_trace(
    go.Pie(labels=failure_counts.index, values=failure_counts.values,
           marker_colors=px.colors.qualitative.Pastel,
           hole=0.4, textinfo='percent+label'),
    row=1, col=1
)

# Bar chart
fig.add_trace(
    go.Bar(x=failure_counts.index, y=failure_counts.values,
           marker_color=px.colors.qualitative.Pastel),
    row=2, col=1
)

# Table
fig.add_trace(
    go.Table(
        header=dict(values=list(table_df.columns),
                    fill_color='lightgrey',
                    align='left'),
        cells=dict(values=[table_df[col] for col in table_df.columns],
                   fill_color='white',
                   align='left',
                   font=dict(size=10)),
        columnwidth=[400, 150, 80, 200]
    ),
    row=3, col=1
)

fig.update_layout(height=1000, showlegend=True, title_text="LLM Stress Test Failure Dashboard")

# Ensure reports folder exists
os.makedirs('reports', exist_ok=True)

# Save full dashboard as one HTML file
fig.write_html("reports/failure_dashboard_full.html")

print("Dashboard with charts and table saved to reports/failure_dashboard_full.html")
