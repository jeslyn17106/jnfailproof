import time
import pandas as pd
from transformers import pipeline

# ===== 1. Load local model =====
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
print(f"Loading model {model_name}...")
classifier = pipeline("sentiment-analysis", model=model_name)

# ===== 2. Read test cases =====
test_cases = pd.read_csv("test_cases.csv")
print(f"Loaded {len(test_cases)} test cases.")

# ===== 3. Safety check function =====
def safety_shutdown_check(prompt):
    banned_words = ["hack", "attack", "kill", "explode", "ass", "a$$", "fuvk", "f*ck", "fuck"]
    if any(word in prompt.lower() for word in banned_words):
        raise RuntimeError("POLICY VIOLATION: Prompt contains banned words.")

# ===== 4. Run stress tests =====
results = []
for i, row in test_cases.iterrows():
    prompt = row["prompt"]

    start_time = time.time()
    try:
        # Safety check BEFORE running model
        safety_shutdown_check(prompt)

        # Model inference
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
        print(f"[{i+1}/{len(test_cases)}] ❌ {prompt} CRASHED: {e}")

# ===== 5. Save results =====
df_results = pd.DataFrame(results)
df_results.to_csv("stress_results.csv", index=False)
df_results.to_json("stress_results.json", orient="records", indent=2)

print("✅ Stress test completed. Results saved.")



