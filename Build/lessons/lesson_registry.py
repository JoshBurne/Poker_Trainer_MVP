# lessons/lesson_registry.py

from lessons.lesson_rfi_easy import EasyRFILesson

LESSON_REGISTRY = {
    "Easy RFI": EasyRFILesson # Reference to the class
    # Add more lessons here like:
    # "RFI Edge Cases": MediumRFILesson(),
    # "Post-Flop CBets": CBetLesson(),
}
