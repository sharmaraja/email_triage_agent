import pandas as pd
from config import DATA_FILE, FEEDBACK_FILE

def load_emails(n=50) -> pd.DataFrame:
    """Load first N emails from CSV."""
    df = pd.read_csv(DATA_FILE)
    return df.head(n)

def log_feedback(email_id: int, llm_output: dict, feedback: dict):
    """Append HITL feedback to log CSV for future use (e.g., few-shot)."""
    log_entry = {
        'email_id': email_id,
        'llm_sentiment': llm_output['sentiment'],
        'llm_urgency': llm_output['urgency'],
        'llm_draft': llm_output['draft_response'],
        'feedback_approved': feedback['approved'],
        'corrected_sentiment': feedback['corrected_sentiment'],
        'corrected_urgency': feedback['corrected_urgency'],
        'edited_draft': feedback['edited_draft']
    }
    # Append to CSV (create if not exists)
    try:
        existing = pd.read_csv(FEEDBACK_FILE)
        updated = pd.concat([existing, pd.DataFrame([log_entry])], ignore_index=True)
    except FileNotFoundError:
        updated = pd.DataFrame([log_entry])
    updated.to_csv(FEEDBACK_FILE, index=False)
    print(f"Feedback logged for email {email_id}.")