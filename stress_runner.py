import time
import pandas as pd
from transformers import pipeline

# ===== 1. Load local free model =====
# Using distilbert-base-uncased as an example for text classification
# You can replace with another model (like text generation) if needed
model_name = "distilbert-base-uncased-finetuned-sst-2-english"  # Sentiment analysis
print(f"Loading model {model_name}...")
classifier = pipeline("sentiment-analysis", model=model_name)

# ===== 2. Read test cases =====
test_cases = pd.read_csv("test_cases.csv")  # assumes 'prompt' column
print(f"Loaded {len(test_cases)} test cases.")

# ===== 3. Run stress tests =====
results = []
for i, row in test_cases.iterrows():
    prompt = row["prompt"]  # adjust column name if needed

    start_time = time.time()
    try:
        output = classifier(prompt)
        latency = round(time.time() - start_time, 3)

        results.append({
            "prompt": prompt,
            "response": output,
            "latency_sec": latency,
            "error": None
        })
        print(f"[{i+1}/{len(test_cases)}] ✅ {prompt} -> {output} ({latency}s)")

    except Exception as e:
        latency = round(time.time() - start_time, 3)
        results.append({
            "prompt": prompt,
            "response": None,
            "latency_sec": latency,
            "error": str(e)
        })
        print(f"[{i+1}/{len(test_cases)}] ❌ {prompt} ERROR: {e}")

# ===== 4. Save results =====
df_results = pd.DataFrame(results)
df_results.to_csv("results/stress_results.csv", index=False)
df_results.to_json("results/stress_results.json", orient="records", indent=2)

print("✅ Stress test completed. Results saved in results/")
