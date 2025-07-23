# lessons/lesson_rfi_easy.py

import random
from lessons.lesson_base import Lesson
from strategy.rfi_chart import get_hand_code, is_in_rfi_range
from utils.positions import get_position_name
from logic.deal import deal_deck
import streamlit as st



class EasyRFILesson(Lesson):
    def run(self):
        st.title("📖 Easy RFI Lesson")
        
        if "lesson_hand" not in st.session_state:
            st.session_state.lesson_hand = None
        if "lesson_position" not in st.session_state:
            st.session_state.lesson_position = None

        if st.button("Deal Lesson Hand"):
            deck = deal_deck()
            st.session_state.lesson_hand = deck[:2]
            st.session_state.lesson_position = 4  # e.g. UTG for now (can make dynamic later)

        if st.session_state.lesson_hand:
            pos_name = get_position_name(st.session_state.lesson_position)
            st.subheader(f"Your Position: {pos_name}")
            st.write("Your Hand:", " | ".join(st.session_state.lesson_hand))

            action = st.radio("What's your move?", ["Fold", "Call", "Raise"])

            if st.button("Submit"):
                st.write(f"You chose to **{action}** with {st.session_state.lesson_hand}")
                # Add feedback logic here later

        else:
            st.info("Click 'Deal Lesson Hand' to start.")
