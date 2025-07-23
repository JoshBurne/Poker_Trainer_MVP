# Build/core/game_engine.py

from strategy.rfi_chart import get_hand_code, is_in_rfi_range
from utils.positions import get_position_name

def evaluate_rfi_action(hand, position, action):
    """
    Evaluates the RFI decision and returns feedback message + result status.
    """
    card1, card2 = hand
    hand_code = get_hand_code(card1, card2)
    pos_name = get_position_name(position)

    if action == "Raise":
        if pos_name in ["Big Blind (BB)", "Small Blind (SB)"]:
            return f"ℹ️ {pos_name} is not a typical RFI position. Raise strength depends on action before you.", "neutral"
        elif is_in_rfi_range(pos_name, hand_code):
            return f"✅ Good raise! {hand_code} is in the RFI range for {pos_name}.", "correct"
        else:
            return f"❌ {hand_code} is not a recommended raise from {pos_name}.", "incorrect"

    elif action == "Fold":
        if pos_name in ["Big Blind (BB)", "Small Blind (SB)"]:
            return f"🗑️ You folded. Click 'Next Hand' to continue.", "neutral"
        elif is_in_rfi_range(pos_name, hand_code):
            return f"❌ {hand_code} is a hand you should raise from {pos_name}. Folding is a mistake.", "incorrect"
        else:
            return f"🗑️ You folded. Click 'Next Hand' to continue.", "neutral"

    elif action == "Call":
        return f"❌ Calling is not part of a standard RFI strategy. You should fold or raise.", "incorrect"

    return f"⚠️ Unknown action.", "neutral"
