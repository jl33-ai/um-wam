import streamlit as st

from src.utils.math import calculate_wam


def _handle_add_grade():
    st.session_state.grades.append({'grade': 50, 'credit_points': 12.5})


def _handle_remove_grade():
    if len(st.session_state.grades) > 1:
        st.session_state.grades.pop()


def _handle_add_pass_fail_subject():
    st.session_state.grades.append({'grade': 0, 'credit_points': 12.5})


def render_toolbar():
    with st.container():
        btn_add_subject, btn_remove_subject, btn_add_pass_fail_subject = st.columns([1, 1, 1], gap="small")

        with btn_add_subject:
            st.button('Add Subject', on_click=_handle_add_grade, type="primary")

        with btn_remove_subject:
            st.button('Add Pass/Fail Subject', on_click=_handle_add_pass_fail_subject)

        with btn_add_pass_fail_subject:
            st.button('Remove Subject', on_click=_handle_remove_grade)
    if st.session_state.grades:
        wam, total_course_credit = calculate_wam(st.session_state.grades)
        st.markdown(f'**Total credit points:** `{total_course_credit}`')
        st.markdown(f"### Your current WAM is **`{wam:.3f}`**")
