# Imports
import smtplib
import imaplib
import email
from datetime import datetime
import config

# Define function to connect to an email mailbox
def connect_email_inbox(imap_host: str, user_email: str, app_password: str):
    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(user_email, app_password)
    mail.select("inbox")
    return mail

# Define function to build IMAP search queries
def build_search_query(subject=None, since=None, from_email=None):
    query_parts = []
    if subject:
        query_parts.append(f'SUBJECT "{subject}"')
    if since:
        query_parts.append(f'SINCE "{since}"')
    if from_email:
        query_parts.append(f'FROM "{from_email}"')
    return " ".join(query_parts) if len(query_parts) > 0 else None

# Define function to send workout email
def send_workout_email(smtp_host, smtp_port, imap_host: str, user_email: str, app_password: str, workout_plan: str):        
    today = datetime.now().strftime('%Y-%m-%d')
    connect_email_inbox(imap_host, user_email, app_password)
    msg = email.message.EmailMessage()
    msg['From'] = user_email
    msg['To'] = user_email
    msg['Subject'] = f"WORKOUT - {today}"
    body = f"""Hi there! Here's your personalized upper body workout for today:
    
    {workout_plan}
    After completing your workout, please reply to this email with:
    1. What exercises you actually completed
    2. Number of sets and reps for each exercise (e.g., "3x10, 4x8")
    3. Weights used for each exercise (e.g., "Bench: 135lbs, Rows: 95lbs")
    4. Completion percentage (e.g., "100%" or "80%")
    
    For example, "Bench press 3x10 at 135lbs 100%, Rows 4x8 at 95lbs 80%"

    Keep crushing those goals! 💪

    Your AI Fitness Coach"""
    
    msg.set_content(body)
    
    send_email(smtp_host, smtp_port, user_email, app_password, msg)

# Define function to check/return email responses
def check_email_responses(imap_host: str, user_email: str, app_password: str) -> list:
    mail = connect_email_inbox(imap_host, user_email, app_password)
    today = datetime.now().strftime('%Y-%m-%d')
    search_query = build_search_query(
        subject=f"Re: WORKOUT - {today}",
        from_email=user_email
    )
    result, data = mail.search(None, search_query)
    responses = []
    if data[0]:
        email_ids = data[0].split()
        for email_id in email_ids:
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            body = extract_email_body(msg)
            responses.append(body)
    return responses

# Define function to extract plain text body from email message
def extract_email_body(msg) -> str:
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode(
                    part.get_content_charset() or "utf-8"
                ).strip()
    else:
        body = msg.get_payload(decode=True).decode().strip()
    return body

# Define function to send an email via SMTP
def send_email(smtp_host: str, smtp_port, user_email: str, app_password: str, reply_msg):
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(user_email, app_password)
    server.send_message(reply_msg)
    server.quit()


# Define function to reply to an email based on subject search
def reply_to_subject(imap_host: str, smtp_host: str, smtp_port, user_email: str, app_password: str, subject_search: str, reply_text: str):
    mail = connect_email_inbox(imap_host, user_email, app_password)
    latest_id = get_latest_email_message(mail, subject_search)
    msg = fetch_email_message(mail, latest_id)
    headers = extract_email_headers(msg)
    reply_msg = compose_reply_email(user_email, headers, reply_text)
    send_email(smtp_host, smtp_port, user_email, app_password, reply_msg)

# Define function to search for latest message by subject
def get_latest_email_message(mail, subject):
    status, data = mail.search(None, subject)
    if data[0]:
        return data[0].split()[-1]
    return None

# Define function to fetch and parse email message by ID
def fetch_email_message(mail, msg_id):
    status, msg_data = mail.fetch(msg_id, "(RFC822)")
    raw_email = msg_data[0][1]
    return email.message_from_bytes(raw_email)

# Define function to extract email headers from a message
def extract_email_headers(msg):
    return {
        "from": msg['From'],
        "subject": msg['Subject'],
        "message_id": msg['Message-ID']
    }

# Define function to compose a reply email message
def compose_reply_email(user_email, orig_headers, reply_text):
    reply = email.message.EmailMessage()
    reply['From'] = user_email
    reply['To'] = orig_headers['from']
    reply['Subject'] = "Re: " + orig_headers['subject']
    reply['In-Reply-To'] = orig_headers['message_id']
    reply['References'] = orig_headers['message_id']
    reply.set_content(reply_text)
    return reply