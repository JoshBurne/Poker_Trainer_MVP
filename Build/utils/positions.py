def get_position_name(pos_id):
    position_map = {
        1: "Button (BTN)",
        2: "Small Blind (SB)",
        3: "Big Blind (BB)",
        4: "Under The Gun (UTG)",
        5: "Under The Gun +1 (UTG+1)",
        6: "Under The Gun +2 (UTG+2)",
        7: "Lojack (LJ)",
        8: "Hijack (HJ)",
        9: "Cutoff (CO)"
    }
    return position_map.get(pos_id, "Unknown")