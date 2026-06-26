from enum import Enum

class HabitCategory(Enum):
    STUDY = "Study Habits"
    CODING = "Coding Habits"
    ENTERTAINMENT = "Entertainment Habits"
    SLEEP = "Sleep-Related Habits"
    MUSIC = "Music Habits"
    LEARNING = "Learning Habits"
    PROCRASTINATION = "Procrastination Habits"
    PRODUCTIVITY = "Productivity Habits"

# Constants for detection
MIN_SESSIONS_FOR_ROUTINE = 3
ROUTINE_TIME_TOLERANCE_MINUTES = 60
MAX_GAP_FOR_SEQUENCE_MINUTES = 60
