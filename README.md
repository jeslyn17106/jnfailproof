# jnfailproof
hiii this project is to help us reach a failproof llm by stress testing it  by nadiya and jeslyn
aka jnsyndicate

Goal:
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

<3 to set up and run
(in powershell on windows)
git clone https://github.com/jeslyn17106/jnfailproof.git
cd jnfailproof

<3 create a python virtual environment
python -m venv venv
.\venv\Scripts\Activate

<3 install dependencies
pip install -r requirements.txt

<3 running our testcase generator
python test_generator.py

<3 running our stress runner
python stress_runner.py

<3 view our failure dashboard
python dashboard.py

currently the dashboard runs a web app on a url link which will be generated

 http://127.0.0.1:8050


but for this the initial steps must be completed





