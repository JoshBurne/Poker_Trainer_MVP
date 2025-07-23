# lessons/lesson_base.py

class Lesson:
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError("Each lesson must implement a run()  method.")
    
    
    def get_prompt(self):
        """Returns the text that prompts the user for input."""
        raise NotImplementedError

    def get_hand(self):
        """Returns a hand dictionary and position ID (int)."""
        raise NotImplementedError

    def evaluate(self, action, hand, position):
        """
        Evaluates user's action.
        Returns: (is_correct: bool, feedback_message: str)
        """
        raise NotImplementedError
