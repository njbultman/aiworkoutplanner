# Imports
from datetime import datetime
import email_utils
import llm_utils
import config
import pandas as pd

# First, check if today's workout response is already recorded
print("Checking if workout response needed...")
df_check = pd.read_csv(config.WORKOUT_HISTORY_FILE)
today_str = datetime.now().strftime('%Y-%m-%d')
# If today's date is already in the date column, exit
if today_str in df_check['date'].values:
    print("Workout response for today already recorded.")
# Otherwise, get response, parse, save, and reply
else:
    print("No workout response for today found. Proceeding to check emails.")
    responses = email_utils.check_email_responses(config.IMAP_HOST, config.EMAIL, config.EMAIL_APP_PASSWORD)
    if not responses:
        print("No new workout responses found.")
    else:
        parsed_data = llm_utils.agent_parse_workout_feedback(config.MODEL_NAME, responses[0])
        temp_df = pd.DataFrame(parsed_data)
        temp_df['date'] = datetime.now().strftime('%Y-%m-%d')
        df = pd.read_csv(config.WORKOUT_HISTORY_FILE)
        df = pd.concat([df, temp_df], ignore_index=True)
        df.to_csv(config.WORKOUT_HISTORY_FILE, index=False)
        email_utils.reply_to_subject(config.IMAP_HOST,
                                     config.SMTP_HOST,
                                     config.SMTP_PORT,
                                     config.EMAIL,
                                     config.EMAIL_APP_PASSWORD,
                                     email_utils.build_search_query(subject=f"WORKOUT - {today_str}"),
                                     "Latest successful workout recorded.")

