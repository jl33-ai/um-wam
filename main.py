import streamlit as st

from src.components.autofill import autofill_from_screenshot
from src.components.grades import render_grades
from src.components.graphs import data_visualization
from src.components.required_grades import required_grades_calculator
from src.components.sidebar import render_sidebar
from src.components.toolbar import render_toolbar

st.set_page_config(page_title="University WAM Calculator", initial_sidebar_state="collapsed")

st.write("## Calculate your Weighted Average Mark (WAM)")

if 'grades' not in st.session_state:
    st.session_state.grades = [{'grade': 50, 'credit_points': 12.5}]

if 'show_required_grades_calculator' not in st.session_state:
    st.session_state.show_required_grades_calculator = False

if 'show_auto_fill_from_screenshot' not in st.session_state:
    st.session_state.show_auto_fill_from_screenshot = False

render_sidebar()

render_grades()

render_toolbar()

st.markdown("---")

st.write('### More tools')

autofill_from_screenshot()

required_grades_calculator()

data_visualization()
