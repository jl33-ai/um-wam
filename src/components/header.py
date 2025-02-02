import streamlit as st


def render_head():
    st.set_page_config(page_title="University WAM Calculator", initial_sidebar_state="collapsed")
    st.write("## Calculate your Weighted Average Mark (WAM)")
