import streamlit as st
import random

# ----------------------------
# Helper Functions
# ----------------------------

def deal_hand():
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [rank + suit for rank in ranks for suit in suits]
    random.shuffle(deck)
    return {
        "hand": deck[:2],
        "flop": deck[2:5],
        "turn": deck[5:6],
        "river": deck[6:7]
    }

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

# ----------------------------
# Session State Init
# ----------------------------

if "hand" not in st.session_state:
    st.session_state.hand = None

if "position" not in st.session_state:
    st.session_state.position = None

if "action_submitted" not in st.session_state:
    st.session_state.action_submitted = False

if "selected_action" not in st.session_state:
    st.session_state.selected_action = None

if "show_flop" not in st.session_state:
    st.session_state.show_flop = False

# ----------------------------
# UI
# ----------------------------

st.title("🃏 Poker Pre-Flop Trainer")

# Deal new hand manually (first time or after "Next Hand")
if st.button("Deal New Hand") or st.session_state.get("reset_next"):
    st.session_state.hand = deal_hand()
    st.session_state.position = random.randint(1, 9)
    st.session_state.selected_action = None
    st.session_state.action_submitted = False
    st.session_state.show_flop = False
    st.session_state.reset_next = False  # clear flag after using it
    st.session_state.folded = False
    st.session_state.submission_message = ""
    st.session_state.reset_next = False

# Show game state
if st.session_state.hand:
    pos_name = get_position_name(st.session_state.position)
    st.subheader(f"Your position: {pos_name}")
    st.write("Your hand:", "🃏 " + " | ".join(st.session_state.hand["hand"]))


    if "folded" not in st.session_state:
        st.session_state.folded = False
    if "submission_message" not in st.session_state:
        st.session_state.submission_message = ""


    # --- Case 1: User has not submitted an action yet ---
    if not st.session_state.action_submitted:
        st.session_state.selected_action = st.radio(
            "What's your move?",
            ["Fold", "Call", "Raise"],
            key="action_radio"
        )

        if st.button("Submit Action"):
            st.session_state.action_submitted = True

            if st.session_state.selected_action == "Fold":
                st.session_state.folded = True
                st.session_state.show_flop = False
                st.session_state.submission_message = "🗑️ You folded. Click 'Next Hand' to continue."
            else:
                st.session_state.folded = False
                st.session_state.show_flop = True
                st.session_state.submission_message = f"✅ You chose to {st.session_state.selected_action}."
            
            st.rerun()
                

    # --- Case 2: Folded – show "Next Hand" button only ---
    elif st.session_state.folded:
        st.warning(st.session_state.submission_message)
        if st.button("Next Hand"):
            st.session_state.reset_next = True
            st.rerun()


    # --- Case 3: Called or Raised – show the flop ---
    elif st.session_state.show_flop:
        st.success(st.session_state.submission_message)
        st.subheader("Flop:")
        st.write("🃏 " + " | ".join(st.session_state.hand["flop"]))

else:
    st.write("Click **Deal New Hand** to begin.")
