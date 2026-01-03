# aiworkoutplanner

## Overview

aiworkoutplanner is an AI-powered workout planner that uses OpenAI and Pydantic AI to generate personalized upper body strength workouts and track your progress via email. It monitors an email inbox for workout-related conversations and handles two types of interactions:

- **Workout generation**: Creates AI-powered workouts based on your exercise history and weight progression
- **Progress tracking**: Parses your workout completion responses using Pydantic AI for structured data validation and updates a CSV file `workout_history.csv` to keep track of progression.

The system learns from your completion rates and weight consistency to recommend progressive overload, helping you build strength systematically while providing motivational quotes to keep you inspired. The integration of Pydantic AI ensures robust type safety and automatic validation of workout feedback data.

## Key Files

- `src/send_workout.py` — generates and emails personalized workouts
- `src/check_responses.py` — processes workout completion responses and updates history
- `src/config.py` — static configuration and environment variables
- `src/email_utils.py` — IMAP/SMTP helpers and email utilities with security filtering
- `src/llm_utils.py` — LLM agent functions for workout generation and Pydantic AI-powered response parsing
- `src/models.py` — Pydantic models for structured workout feedback validation
- `data/workout_history.csv` — exercise log with completion data, weights, and progression tracking

## Environment & Setup

Create and activate a Python virtual environment.

Install required packages: `openai`, `pydantic-ai`, and `pandas` (and any other dependencies in `src/`)

Provide these environment variables:
- `IMAP_HOST` — IMAP server host
- `SMTP_HOST` — SMTP server host  
- `SMTP_PORT` — SMTP port (integer)
- `EMAIL` — the sending/receiving email address
- `EMAIL_APP_PASSWORD` — app-specific password for SMTP/IMAP authentication
- `OPENAI_API_KEY` — OpenAI API key

## Getting Started

The system operates on a simple cycle: receive workout → complete workout → report back → get next workout.

To start, cd into the src folder and generate your first workout:

```bash
source venv/bin/activate
cd src
python send_workout.py
```

This will email you a personalized upper body workout with specific weight recommendations and a motivational quote to the email specified via the environment variables.

After completing your workout, reply to the email in a similar format to the below:

```
Completed:
bench press 3x8 45lbs 100%
rows 3x10 20lbs 100%
incline dumbbell press 45lbs 80%
```

Then process your response:

```bash
python check_responses.py
```

This will parse your feedback, update your workout history in `workout_history.csv`, and send a confirmation email letting you know the workout was saved.

Once you feel comfortable with the process, you can schedule this to run periodically via cron. The system will only call OpenAI when needed (when sending an initial workout and when a reply is found that it needs to parse), keeping costs low.

## Notes

- This has been tested with Gmail on a Raspberry Pi using the GPT-4o Mini model
- While environment variables can be overwritten in config.py with hard-coded variables, this is strongly discouraged for security reasons
- The system analyzes your last 24 records (assuming six items in a workout, it is about the last three workouts) to make intelligent progression recommendations.
- Only emails from your own email address are processed to ensure results are as expected

Here is an example cron configuration to send workouts Mon/Wed at 6 AM and check responses at 7:30 AM:

```bash
crontab -e
0 6 * * 1,3 . PATH/TO/PROJECT/aiworkoutplanner/venv/bin/activate && cd PATH/TO/PROJECT/aiworkoutplanner/src && PATH/TO/PROJECT/aiworkoutplanner/venv/bin/python send_workout.py > /dev/null 2>&1
30 7 * * 1,3 . PATH/TO/PROJECT/aiworkoutplanner/venv/bin/activate && cd PATH/TO/PROJECT/aiworkoutplanner/src && PATH/TO/PROJECT/aiworkoutplanner/venv/bin/python check_responses.py > /dev/null 2>&1
```

## Behavior & Workout Flow

1. **Workout Generation**: AI analyzes your recent workouts, identifies weight progression patterns, and creates a personalized upper body strength routine with specific weight recommendations

2. **Email Delivery**: Workout is sent to your email with subject "WORKOUT - YYYY-MM-DD" format, including exercises, sets/reps, recommended weights, and a motivational quote

3. **Completion Tracking**: You complete the workout (modifying as needed) and reply describing what you actually did

4. **Progress Analysis**: Pydantic AI parses your response with automatic validation to extract exercises, sets/reps, weights used, and completion percentage, then saves this structured data with type safety guarantees

The system creates a closed feedback loop where each workout builds on your actual performance data, ensuring recommendations stay realistic and progressive.