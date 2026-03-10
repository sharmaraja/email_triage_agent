# Run this once to generate sample_emails.csv with 50 dummy emails
import pandas as pd
import random
import string

def generate_dummy_text(length=200):
    words = [''.join(random.choices(string.ascii_letters + ' .,!?')) for _ in range(20)]
    return ' '.join(words)[:length]

subjects = [
    "Meeting tomorrow", "Invoice payment due", "Newsletter update", "Spam offer", "Urgent issue",
    "Feedback on product", "Sale alert", "Conference invite", "Bug report", "Promotion"
] * 5

emails = []
for i in range(50):
    subject = random.choice(subjects)
    body = generate_dummy_text()
    sender = f"user{random.randint(1,100)}@example.com"
    email_text = f"Subject: {subject}\nFrom: {sender}\n\n{body}"
    sentiment = random.choice(["positive", "neutral", "negative"])
    urgency = random.choice(["urgent", "non-urgent", "spam"])
    emails.append({
        'id': i+1,
        'email_text': email_text,
        'sentiment': sentiment,  # Ground truth for eval (optional)
        'urgency': urgency
    })

df = pd.DataFrame(emails)
df.to_csv('sample_emails.csv', index=False)
print(f"Generated sample_emails.csv with {len(df)} emails.")