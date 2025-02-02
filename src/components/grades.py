import streamlit as st


def render_grades():
    """ Render grade and credit points inputs """
    col1_grades, col2_grades = st.columns(2)

    for i, grade_info in enumerate(st.session_state['grades']):
        with col1_grades:
            if grade_info['grade'] == 0:
                st.text_input(f'Subject {i + 1}', value='Pass/Fail', key=f'grade_{i}')
            else:
                st.session_state['grades'][i]['grade'] = st.number_input(f'Subject {i + 1}', value=grade_info['grade'],
                                                                         key=f'grade_{i}', min_value=0, max_value=100)
        with col2_grades:
            st.session_state['grades'][i]['credit_points'] = st.number_input(f'Credit Points',
                                                                             value=grade_info['credit_points'],
                                                                             key=f'credit_{i}')
