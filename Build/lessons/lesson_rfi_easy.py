# Build/lessons/lesson_rfi_easy.py

import random
from lessons.lesson_base import Lesson
from logic.deal import initialize_deck
from lessons.lesson_ui import render_simple_rfi_lesson
import streamlit as st

class EasyRFILesson(Lesson):
    def run(self):
        if st.session_state.get("reset_next", True):
            deck = initialize_deck()
            player_hand = deck[:2]
            st.session_state.lesson_hand = player_hand
            st.session_state.lesson_position = 4  # UTG
            st.session_state.action_submitted = False
            st.session_state.lesson_result = None
            st.session_state.reset_next = False

        render_simple_rfi_lesson(
            hand=st.session_state.lesson_hand,
            position=st.session_state.lesson_position
        )
