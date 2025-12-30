# Imports
from openai import OpenAI
import json

# Define agent to generate a workout plan based on user history
def agent_generate_workout_plan(model_name: str, history_string: str) -> str:
    client = OpenAI()
    prompt = f"""
    User Profile:
    - Fitness Level: medium
    - Goals: upper body strength
    - Equipment: dumbbells (up to 75lbs), barbell, pull-up bar, bench, cable machine
    - Time per workout: 30-40 minutes
    - Workouts per week: 2
    
    Recent Workout History:
    {history_string}
    
    Create a single upper body strength workout for today. CRITICAL REQUIREMENTS:
    
    1. **Analyze the workout history above** and recommend appropriate weights:
       - Look for exercises where the user has been consistent with the same weight for 2+ sessions
       - If completion rate is high (90%+), suggest 5lb increase
       - If completion rate is low (<80%), maintain or slightly reduce weight
       - For new exercises or if no weight history, suggest conservative starting weights
    
    2. **Exercise Selection**: Focus on compound movements for upper body strength:
       - Bench press, overhead press, rows, pull-ups/lat pulldowns
       - Include specific weight recommendations based on the progression analysis above
    
    3. **Format**: For each exercise, specify:
       - Exercise name (sets x reps) - RECOMMENDED WEIGHT: XXX lbs
    
    4. **Progressive Overload**: Make intelligent weight recommendations based on the user's history patterns.
    
    5. **Motivational Quote**: End the workout with an inspiring fitness/strength quote to motivate the user.
    
    Keep it realistic for a 30-40 minute session. Focus on strength progression over volume, and do not recommend more than seven exercises.
    """
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an expert strength coach specializing in progressive overload and upper body development. Analyze workout history patterns to make intelligent weight progression recommendations. Always provide specific weight recommendations based on training history. End every workout with an inspiring quote."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Define agent to parse workout feedback from email responses into appropriate JSON object
def agent_parse_workout_feedback(model_name: str, feedback: str) -> dict:
    client = OpenAI()
    prompt = f"""
    Parse this workout feedback email and extract the key information. Return a JSON object with these exact keys:
    - completed_exercises: list of strings describing what exercises were completed. Each exercise should be its own item in the list
    - sets_reps: list of strings describing sets and reps for each exercise in completed_exercises (e.g., "3x10", "4x8")
    - weights_used: List of integers corresponding to weights for each exercise in completed_exercises
    - completion_percentage: integer from 0-100 (default 100 if not mentioned) for each exercise in completed_exercises
    
    Email feedback:
    {feedback}
    
    Return only valid JSON, no other text.
    """
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a data extraction assistant. Parse workout feedback emails and return structured JSON data. Always return valid JSON with the exact keys requested."},
            {"role": "user", "content": prompt}
        ]
    )
    message = response.choices[0].message.content.strip()
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        catch_response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a JSON parsing assistant that helps correct invalid JSON. Only return the corrected JSON, no other text."},
                {"role": "user", "content": f"Here is the invalid JSON - correct it: {message}."}
            ]
        )
        return json.loads(catch_response.choices[0].message.content.strip())