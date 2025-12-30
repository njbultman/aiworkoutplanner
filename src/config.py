# Imports
import os

# Static configuration variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
EMAIL = os.environ.get("EMAIL")
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD")
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT"))
IMAP_HOST = os.environ.get("IMAP_HOST")
WORKOUT_HISTORY_FILE = "../data/workout_history.csv"
MODEL_NAME = "gpt-4o-mini"