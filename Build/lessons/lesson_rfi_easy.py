# lessons/lesson_rfi_easy.py

import random
from lessons.lesson_base import Lesson
from strategy.rfi_chart import get_hand_code, is_in_rfi_range, get_position_name

class EasyRFILesson(Lesson):
    def get_prompt(self):
        return "You're playing pre-flop. Should you Fold, Call or Raise?"

    def get_hand(self):
        # Only use positions where RFI is valid (exclude SB = 2, BB = 3)
        rfi_positions = [1, 4, 5, 6, 7, 8, 9]  # BTN, UTG → CO
        hands = [("A♠", "K♠"), ("Q♦", "Q♣"), ("J♠", "J♥"), ("K♠", "Q♠")]
        hand = random.choice(hands)
        position = random.choice(rfi_positions)
        return {"player": list(hand)}, position

    def evaluate(self, action, hand, position):
        # Defensive: if SB or BB somehow gets through, block it
        if position in [2, 3]:
            pos_name = get_position_name(position)
            return False, f"❌ {pos_name} is not an RFI position. Use defend/3-bet logic instead."

        card1, card2 = hand["player"]
        hand_code = get_hand_code(card1, card2)
        pos_name = get_position_name(position)

        if action == "Raise":
            if is_in_rfi_range(pos_name, hand_code):
                return True, f"✅ Good raise! {hand_code} is in the RFI range for {pos_name}."
            else:
                return False, f"❌ {hand_code} is not a recommended RFI (Raise First In) from {pos_name}."
        elif action == "Fold":
            if is_in_rfi_range(pos_name, hand_code):
                return False, f"❌ {hand_code} is a raising hand from {pos_name}. Folding is a mistake."
            else:
                return True, f"✅🗑️ You folded. {hand_code} is not in the recommended range from {pos_name}."
        else:
            return False, f"ℹ️ Calling is not recommended here. You should either raise or fold in most RFI spots."
