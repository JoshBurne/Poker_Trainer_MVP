# Build/lessons/lesson_ui.py

import streamlit as st
from core.game_engine import evaluate_rfi_action
from utils.positions import get_position_name

def render_simple_rfi_lesson(hand, position):
    """
    A shared UI flow for simple preflop RFI lessons.
    """
    pos_name = get_position_name(position)
    st.subheader(f"Your position: {pos_name}")
    st.write("Your hand:", "🃏 " + " | ".join(hand))

    if not st.session_state.get("action_submitted"):
        st.session_state.selected_action = st.radio(
            "What's your move?",
            ["Fold", "Call", "Raise"],
            key="lesson_action_radio"
        )

        if st.button("Submit Action"):
            st.session_state.action_submitted = True
            feedback, result = evaluate_rfi_action(hand, position, st.session_state.selected_action)
            st.session_state.lesson_result = result
            st.session_state.submission_message = feedback
            st.rerun()

    elif st.session_state.get("lesson_result"):
        result = st.session_state.lesson_result
        msg = st.session_state.submission_message
        if result == "correct":
            st.success(msg)
        elif result == "incorrect":
            st.error(msg)
        else:
            st.warning(msg)

        if st.button("Next Hand"):
            st.session_state.reset_next = True
            st.rerun()
