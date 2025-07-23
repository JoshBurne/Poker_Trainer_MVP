# strategy/rfi_chart.py

# Simple example RFI chart for 3 positions only (expand later)
RFI_CHART = {
    "Under The Gun (UTG)": [
        "AA", "KK", "QQ", "JJ", "TT", "99",
        "AKs", "AQs", "AJs", "KQs"
    ],
    "Under The Gun +1 (UTG+1)": [
        "AA", "KK", "QQ", "JJ", "TT", "99", "88",
        "AKs", "AQs", "AJs", "KQs", "ATs", "KJs",
        "AQo", "AJo"
    ],
    "Under The Gun +2 (UTG+2)": [
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77",
        "AKs", "AQs", "AJs", "ATs", "KQs", "KJs", "QJs",
        "AQo", "AJo", "KQo"
    ],
    "Lojack (LJ)": [
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66",
        "AKs", "AQs", "AJs", "ATs", "A9s", "KQs", "KJs", "QJs", "JTs",
        "AQo", "AJo", "KQo"
    ],
    "Hijack (HJ)": [
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55",
        "AKs", "AQs", "AJs", "ATs", "A9s", "KQs", "KJs", "QJs", "JTs", "T9s", "98s",
        "AQo", "AJo", "KQo", "KJo"
    ],
    "Cutoff (CO)": [
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
        "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A5s", "KQs", "KJs", "QJs", "JTs", "T9s", "98s",
        "AQo", "AJo", "KQo", "KJo", "QJo"
    ],
    "Button (BTN)": [
        "All pairs",  # We'll handle this via special rule
        "All suited Aces",  # A2s–AKs
        "A2o+", "K9s+", "Q9s+", "J9s+", "T9s", "98s", "87s", "76s", "65s", "54s",
        "KTo+", "QTo+", "JTo"
    ],
    "Small Blind (SB)": [
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66",
        "AKs", "AQs", "AJs", "ATs", "KQs", "QJs", "JTs",
        "AQo", "AJo", "KQo"
    ],
    "Big Blind (BB)": []  # Not used in RFI logic, but placeholder for future defense logic
}

def get_hand_code(card1, card2):
    """
    Convert two cards (e.g., 'A♠', '10♦') to a hand code (e.g., 'AKs', 'TT', 'KQo').
    """
    rank_map = {
        "2": "2", "3": "3", "4": "4", "5": "5", "6": "6",
        "7": "7", "8": "8", "9": "9", "10": "T", "J": "J",
        "Q": "Q", "K": "K", "A": "A"
    }
    ranks_order = list(rank_map.values())

    def extract_rank(card):
        for r in sorted(rank_map.keys(), key=len, reverse=True):
            if card.startswith(r):
                return rank_map[r]
        return "?"

    rank1 = extract_rank(card1)
    rank2 = extract_rank(card2)
    suit1 = card1.replace(rank1, "")
    suit2 = card2.replace(rank2, "")

    # Sort ranks by value so AJo not JAo
    if ranks_order.index(rank1) > ranks_order.index(rank2):
        rank1, rank2 = rank2, rank1
        suit1, suit2 = suit2, suit1

    if rank1 == rank2:
        return f"{rank1}{rank1}"  # e.g., "TT"
    suited = "s" if suit1 == suit2 else "o"
    return f"{rank1}{rank2}{suited}"  # e.g., "AKs", "QTo"



def is_in_rfi_range(position_name, hand_code):
    """
    Check if a hand code (like AJo) is in the RFI range for the position.
    Supports wildcards like 'All pairs' or 'All suited Aces'.
    """
    range_list = RFI_CHART.get(position_name, [])
    if hand_code in range_list:
        return True

    # Handle wildcard rules
    if "All pairs" in range_list and len(hand_code) == 2 and hand_code[0] == hand_code[1]:
        return True

    if "All suited Aces" in range_list and hand_code.startswith("As"):
        return True

    return False
