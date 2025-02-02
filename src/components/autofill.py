import streamlit as st

from src.config import MAX_FILE_SIZE_MB
from src.services.ocr import extract_list_from_image


def populate_grades(grade_list):
    """ Clears the current list and populates it with new grades. """
    st.session_state.grades.clear()
    for _, grade in enumerate(grade_list):
        st.session_state.grades.append({'grade': int(grade), 'credit_points': 12.5})
    if 'upload_widget' in st.session_state:
        st.session_state.show_auto_fill_from_screenshot = False
    st.rerun()


def extract_grades(file):
    """ Extracts grades from columnar screenshot and populates the table. """
    if file is None:
        st.error("No screenshot was uploaded")
        return

    if file.size > MAX_FILE_SIZE_MB:
        st.error("The uploaded screenshot is too large. Please upload an image smaller than 5MB.")
        return

    return extract_list_from_image(file)


def render_autofill_from_screenshot():
    # AUTOFILL FROM SCREENSHOT
    def handle_autofill(file):
        if not file:
            st.error('Please upload a file first')
            return

        grades_list = extract_grades(file)

        if not grades_list:
            st.warning("Couldn't find any grades in the provided screenshot")
            return

        populate_grades(grades_list)

    if st.button('Autofill from Screenshot'):
        st.session_state.show_auto_fill_from_screenshot = True
    if st.session_state.show_auto_fill_from_screenshot:
        file = st.file_uploader("Upload a screenshot of your grades", type=["png", "jpg", "jpeg"])
        if st.button('Autofill'):
            handle_autofill(file)

        example_col1, example_col2 = st.columns([1, 2])

        st.markdown('---')

        with example_col1:
            st.write('#### How to submit')
            st.write("1. Never include **subject codes** or your **student ID**")
            st.write("2. Your screenshot should include only the `marks` column as shown")
            st.write("3. Warning: Autofilling will **overwrite all current grades**")
        with example_col2:
            st.image('static/example_upload_screenshot.gif')
