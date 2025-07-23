# lessons/lesson_registry.py

from lessons.lesson_rfi_easy import EasyRFILesson

LESSON_REGISTRY = {
    "RFI Basics (Easy)": EasyRFILesson(),
    # Add more lessons here like:
    # "RFI Edge Cases": MediumRFILesson(),
    # "Post-Flop CBets": CBetLesson(),
}
