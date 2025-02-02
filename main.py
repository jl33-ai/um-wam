import streamlit as st

from src.components.autofill import render_autofill_from_screenshot
from src.components.grades import render_grades
from src.components.graphs import render_charts
from src.components.header import render_head
from src.components.required_grades import render_required_grades_calculator
from src.components.sidebar import render_sidebar
from src.components.store import configure_store
from src.components.toolbar import render_toolbar

render_head()

configure_store()

render_sidebar()

render_grades()

render_toolbar()

st.markdown("---")

st.write('### More tools')

render_autofill_from_screenshot()

render_required_grades_calculator()

render_charts()
