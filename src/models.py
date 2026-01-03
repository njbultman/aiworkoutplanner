from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class WorkoutFeedback(BaseModel):
    completed_exercises: List[str] = Field(
        description="List of exercises completed during the workout. Each exercise should be described as a separate string item."
    ) 
    sets_reps: List[str] = Field(
        description="Sets and reps for each exercise in completed_exercises (e.g., '3x10', '4x8'). Must correspond to the same order as completed_exercises."
    )
    weights_used: List[Optional[int]] = Field(
        description="Weights used for each exercise in completed_exercises. Use None for bodyweight exercises or when weight is not specified. Must correspond to the same order as completed_exercises."
    )
    completion_percentage: List[int] = Field(
        description="Completion percentage for each exercise in completed_exercises (0-100). Default to 100 if not mentioned. Must correspond to the same order as completed_exercises."
    )
    @field_validator('completion_percentage')
    @classmethod
    def validate_completion_percentage(cls, v):
        for percentage in v:
            if not (0 <= percentage <= 100):
                raise ValueError(f'Completion percentage must be between 0 and 100, got {percentage}')
        return v
    def to_dict(self) -> dict:
        return {
            "completed_exercises": self.completed_exercises,
            "sets_reps": self.sets_reps,
            "weights_used": self.weights_used,
            "completion_percentage": self.completion_percentage
        }