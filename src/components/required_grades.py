import streamlit as st

from src.utils.math import calculate_wam


def calculator(current_wam, num_completed):
    desired_wam = st.slider("Desired WAM", 50, 100, 75)
    remaining_subjects = st.number_input("Number of Remaining Subjects (You may go above 24)", min_value=1,
                                         value=(24 - num_completed))
    if remaining_subjects > 0:
        total_subjects = num_completed + remaining_subjects
        required_average = ((desired_wam * total_subjects) - (current_wam * num_completed)) / remaining_subjects
        st.markdown(f"### Average score needed to achieve a WAM of {desired_wam}: **`{required_average:.2f}`**")
    else:
        st.write("Please enter the number of completed subjects and remaining subjects.")

    st.markdown("---")


def render_required_grades_calculator():
    num_completed = len(st.session_state.grades)
    if st.button('Calculate grades needed for desired WAM'):
        if num_completed:
            st.session_state.show_required_grades_calculator = True
        else:
            st.write('Please add at least one subject first')
    if st.session_state.show_required_grades_calculator:
        current_wam, _ = calculate_wam(st.session_state.grades)
        calculator(current_wam, num_completed)
