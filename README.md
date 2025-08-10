# jnfailproof
hiii welcome to the ultimate ai stress test generator (with a failure analysis dashboard !!!) by nadiya and jeslyn aka jnsyndicate

------------------------------------------------------------------------------------------------------
# Goal:
Create a stress-testing framework that bombards an LLM or agent with edge cases,
malformed inputs, and tricky scenarios—then reports vulnerabilities, failure modes, and
robustness metrics.
Core Features (MVP)
1. Test Case Generator – Produce diverse adversarial inputs: malformed JSON,
misspellings, mixed languages, contradictory instructions, very long inputs, special
characters, and prompt injections.
2. Automated Stress Runner – Feed these cases into the target LLM/agent (via API or
local) and record responses, latency, and errors.
3. Failure Analysis Dashboard – Classify failures (e.g., refusal, crash, incorrect output,
policy violation) and present them in a visual report.
------------------------------------------------------------------------------------------------------

# What is in our repo???

🤍 test_case_generator.py & test_generator.py — Scripts related to generating test cases

🤍 test_cases.csv — Generated test cases data file

🤍 test.py — Your newer test case generator script (v2)

🤍 stress_runner.py — Runs tests on your model, logs results to results/stress_results.csv and .json

🤍 stress.py — Another stress script (double check if needed)

🤍 dashboard.py — Launches the interactive dashboard to visualize results live

🤍 failure_dashboard.py — Generates PDF or static failure reports (optional)

🤍 main.py — Your main orchestration file, probably calling everything sequentially

🤍 requirements.txt — Python dependencies

🤍 results/ — Folder with test results CSV & JSON

🤍 reports/ — Folder for dashboard HTML reports and PDFs

------------------------------------------------------------------------------------------------------
# let's begin :D

🤍 to set up and clone the repo
(in powershell on windows)

git clone https://github.com/jeslyn17106/jnfailproof.git

cd jnfailproof



🤍 create a python virtual environment

python -m venv venv

#Windows PowerShell:

.\venv\Scripts\activate

#Mac/Linux:

source venv/bin/activate

🤍 install dependencies

pip install -r requirements.txt


🤍 running our testcase generator 

( **funfact**: this creates test_cases.csv with over 15 test cases that go from normal inputs to *sneaky* edge cases }:) )

python test.py


🤍 our automated stress runner and interactive failure dashboard that opens automatically cause its cool

python run_all.py

 # or 
 
🤍 running our stress runner on our local ai model *huggingface*

python stress_runner.py


🤍 our failure dashboard (for this we used plotly) (make sure stress_results.csv is at results/stress_results.csv)


python dashboard.py


currently the dashboard runs a web app on a url link which will be generated **once all these steps are done**

 http://127.0.0.1:8050 (dashboard link)

------------------------------------------------------------------------------------------------------
# 🛠 Notes
🤍 If pip or scripts don't work, make sure your virtual environment is activated properly

🤍 If you get missing module errors, install them manually inside venv via pip install <module>

🤍 Make sure folders results and reports exist before running scripts or create them manually

🤍 Use main.py if it orchestrates everything for you






