import streamlit as st


def render_head():
    st.set_page_config(
        page_title="University WAM Calculator",
        initial_sidebar_state="collapsed",
        page_icon="🎓"
    )
    st.write("## Calculate Weighted Average Mark (WAM)")
