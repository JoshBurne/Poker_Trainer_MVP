import streamlit as st

def init_session_state():
    defaults = {
        "hand": None,
        "position": None,
        "action_submitted": False,
        "selected_action": None,
        "show_flop": False,
        "folded": False,
        "submission_message": "",
        "reset_next": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
