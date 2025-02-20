import streamlit as st


def render_head():
    st.set_page_config(
        page_title="University WAM Calculator",
        initial_sidebar_state="collapsed",
        page_icon="🎓",
        menu_items={
            'Report a bug': "https://github.com/jl33-ai/um-wam/issues/new",
            'About': "# Calculate your university weighted average mark (WAM)",
        }
    )
    st.header("Calculate Weighted Average Mark (WAM)")
