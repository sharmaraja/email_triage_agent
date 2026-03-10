from graph import app
from dataset import load_emails
from state import AgentState
import sys

def main():
    print("=== Email Triage AI Agent (HITL) ===")
    emails_df = load_emails(50)
    print(f"Loaded {len(emails_df)} emails. Processing one-by-one.")

    for idx, row in emails_df.iterrows():
        state = AgentState(
            email_id=row['id'],
            original_email=row['email_text'],
            processed_email="",  # Filled by graph
            llm_output={},
            human_feedback={}
        )

        # Run the graph
        final_state = app.invoke(state)

        # Action based on final output
        urgency = final_state['llm_output']['urgency']
        if urgency == 'spam':
            print("Action: Archive as spam.")
        elif urgency == 'urgent':
            print("Action: Flag for immediate attention.")
        else:
            print("Action: Queue for later.")

        # Next email?
        if idx < len(emails_df) - 1:
            cont = input("\nNext email? (y/n/quit): ").lower()
            if cont == 'n' or cont == 'quit':
                print("Stopping early.")
                sys.exit(0)

    print("Processed all emails. Check feedback_log.csv for updates.")

if __name__ == "__main__":
    main()