# email_triage_agent
email_triage_agent using llms with hitl 


**Steps to run this:**

Create the project dir: mkdir email_triage_agent && cd email_triage_agent
Copy the files below.
Install deps: pip install -r requirements.txt
Generate data: python generate_sample_data.py (creates sample_emails.csv with 50 dummy emails).
Set API key: export OPENAI_API_KEY=your_key_here
Run: python main.py → Processes 50 emails one-by-one; provide HITL feedback via console.

**Folder Structure**
email_triage_agent/
├── requirements.txt      # Dependencies
├── config.py             # API/config settings
├── generate_sample_data.py  # Run once to create sample_emails.csv
├── preprocessor.py       # Email text cleaning
├── llm.py                # LangChain LLM chain for structured output
├── state.py              # LangGraph state schema
├── graph.py              # LangGraph workflow definition
├── dataset.py            # CSV load/update for emails & feedback
└── main.py               # Entry point: load data, run graph loop