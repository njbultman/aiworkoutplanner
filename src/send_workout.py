# Imports
import email_utils
import llm_utils
import pandas as pd
import config

# Get workout history
df = pd.read_csv(config.WORKOUT_HISTORY_FILE)
# Get recent workout history as string
recent_workouts = df.tail(24)
history_string = recent_workouts.to_string(index=False) if not recent_workouts.empty else "No workout history yet"
# Generate and send workout plan
workout = llm_utils.agent_generate_workout_plan(config.MODEL_NAME, history_string)
email_utils.send_workout_email(config.SMTP_HOST,
                    config.SMTP_PORT,
                    config.IMAP_HOST,
                    config.EMAIL,
                    config.EMAIL_APP_PASSWORD,
                    workout)
print("Workout email sent successfully.")
