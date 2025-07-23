import streamlit as st
import random

from logic.deal import deal_hand
from state.session import init_session_state

# ----------------------------
# Init session
# ----------------------------
init_session_state()

# ----------------------------
# Title
# ----------------------------
st.title("🃏 Poker Pre-Flop Trainer")

# ----------------------------
# Deal new hand manually
# ----------------------------
if st.button("Deal New Hand") or st.session_state.get("reset_next"):
    st.session_state.hand = deal_hand()
    st.session_state.position = random.randint(1, 9)
    st.session_state.selected_action = None
    st.session_state.action_submitted = False
    st.session_state.show_flop = False
    st.session_state.reset_next = False
    st.session_state.folded = False
    st.session_state.submission_message = ""

# ----------------------------
# Display hand + UI
# ----------------------------
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

if st.session_state.hand:
    pos_name = get_position_name(st.session_state.position)
    st.subheader(f"Your position: {pos_name}")
    st.write("Your hand:", "🃏 " + " | ".join(st.session_state.hand["player"]))

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

    elif st.session_state.folded:
        st.warning(st.session_state.submission_message)
        if st.button("Next Hand"):
            st.session_state.reset_next = True
            st.rerun()

    elif st.session_state.show_flop:
        st.success(st.session_state.submission_message)
        st.subheader("Flop:")
        st.write("🃏 " + " | ".join(st.session_state.hand["flop"]))

else:
    st.write("Click **Deal New Hand** to begin.")
