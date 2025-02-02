import streamlit as st


def configure_store():
    """ Set up the application state """
    if 'grades' not in st.session_state:
        st.session_state.grades = [{'grade': 50, 'credit_points': 12.5}]
    if 'show_required_grades_calculator' not in st.session_state:
        st.session_state.show_required_grades_calculator = False
    if 'show_auto_fill_from_screenshot' not in st.session_state:
        st.session_state.show_auto_fill_from_screenshot = False
