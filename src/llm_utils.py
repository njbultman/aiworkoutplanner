# Imports
from openai import OpenAI
import json
from pydantic_ai import Agent
import models

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
    pydantic_model_name = f"openai:{model_name}"
    workout_parser = Agent(
        pydantic_model_name,
        output_type=models.WorkoutFeedback,
        retries=3,
        system_prompt="""
        You are a workout data extraction specialist. Your job is to parse workout feedback emails and extract structured information.

        CRITICAL INSTRUCTIONS:
        1. Extract ALL exercises mentioned in the feedback, even if partially completed
        2. For each exercise, provide corresponding sets_reps, weights_used, and completion_percentage
        3. All four lists (completed_exercises, sets_reps, weights_used, completion_percentage) must have the same length
        4. Use None for weights_used when no weight is mentioned or for bodyweight exercises
        5. Default completion_percentage to 100 if not explicitly mentioned
        6. For sets_reps, use format like "3x10", "4x8", etc.

        EXAMPLES:
        - "Did 3 sets of 10 bench press at 135lbs" → completed_exercises: ["Bench Press"], sets_reps: ["3x10"], weights_used: [135], completion_percentage: [100]
        - "Pull-ups 3x8, only got 80% through" → completed_exercises: ["Pull-ups"], sets_reps: ["3x8"], weights_used: [None], completion_percentage: [80]
        """
    )
    result = workout_parser.run_sync(feedback)
    return result.output.to_dict()