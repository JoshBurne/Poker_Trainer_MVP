import streamlit as st
import random

from logic.deal import deal_hand
from state.session import init_session_state
from strategy.rfi_chart import get_hand_code, is_in_rfi_range, RFI_CHART
from lessons.lesson_registry import LESSON_REGISTRY
from utils.positions import get_position_name


# ----------------------------
# Init session
# ----------------------------
init_session_state()

# ----------------------------
# Title
# ----------------------------
st.title("🃏 Poker Pre-Flop Trainer")

lesson_names = list(LESSON_REGISTRY.keys())

st.sidebar.header("📚 Select a Lesson")
selected_lesson_name = st.sidebar.selectbox("Choose a lesson:", ["None"] + lesson_names)

st.session_state.selected_lesson = selected_lesson_name if selected_lesson_name != "None" else None

# ----------------------------
# If a lesson is selected, run its logic
# ----------------------------
if st.session_state.selected_lesson:
    selected_lesson = LESSON_REGISTRY[st.session_state.selected_lesson]()
    selected_lesson.run()
    st.stop()  # Prevent rest of UI from loading

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

            card1, card2 = st.session_state.hand["player"]
            hand_code = get_hand_code(card1, card2)
            pos_name = get_position_name(st.session_state.position)

            if st.session_state.selected_action == "Fold":
                st.session_state.folded = True
                st.session_state.show_flop = False

                if pos_name in RFI_CHART and is_in_rfi_range(pos_name, hand_code):
                    st.session_state.submission_message = (
                        f"❌ {hand_code} is a hand you should raise from {pos_name}. Folding is a mistake."
                    )
                else:
                    st.session_state.submission_message = (
                        f"✅🗑️ You folded. {hand_code} is not in the recommended range from {pos_name}."
                    )

            elif st.session_state.selected_action == "Raise":
                st.session_state.folded = False
                st.session_state.show_flop = True

                if pos_name in RFI_CHART:
                    if is_in_rfi_range(pos_name, hand_code):
                        st.session_state.submission_message = (
                            f"✅ Good raise! {hand_code} is in the RFI range for {pos_name}."
                        )
                    else:
                        st.session_state.submission_message = (
                            f"❌ {hand_code} is not a recommended raise from {pos_name}."
                        )
                else:
                    st.session_state.submission_message = (
                        f"ℹ️ {pos_name} is not a raising position in RFI charts. Raise strength depends on previous action."
                    )

            else:  # Call logic
                st.session_state.folded = False
                st.session_state.show_flop = True
                st.session_state.submission_message = f"✅ You chose to Call."

            st.rerun()





    # Show feedback message in the right color
    msg = st.session_state.submission_message
    if "✅" in msg:
        st.success(msg)
    elif "❌" in msg:
        st.error(msg)
    elif "🗑️" in msg:
        st.warning(msg)
    else:
        st.info(msg)

    # Then continue as normal
    if st.session_state.folded:
        if st.button("Next Hand"):
            st.session_state.reset_next = True
            st.rerun()

    elif st.session_state.show_flop:
        st.subheader("Flop:")
        st.write("🃏 " + " | ".join(st.session_state.hand["flop"]))

    else:
        st.write("Click **Deal New Hand** to begin.")
