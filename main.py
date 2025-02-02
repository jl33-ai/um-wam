import streamlit as st

from utils.components import render_all_graphs
from utils.config import MAX_FILE_SIZE_MB
from utils.math import calculate_wam
from utils.ocr import extract_list_from_image

st.set_page_config(page_title="University WAM Calculator", initial_sidebar_state="collapsed")

st.write("## Calculate your Weighted Average Mark (WAM)")


def populate_grades(grade_list):
    """ Clears the current list and populates it with new grades. """
    st.session_state.grades.clear()
    for _, grade in enumerate(grade_list):
        st.session_state.grades.append({'grade': int(grade), 'credit_points': 12.5})
    if 'upload_widget' in st.session_state:
        st.session_state.upload_widget = False
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


if 'grades' not in st.session_state:
    st.session_state.grades = [{'grade': 50, 'credit_points': 12.5}]

if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = False

if 'upload_widget' not in st.session_state:
    st.session_state.upload_widget = False

st.sidebar.markdown("### How your WAM is calculated")
st.sidebar.markdown(
    "See the official [University of Melbourne website](https://students.unimelb.edu.au/your-course/manage-your-course/exams-assessments-and-results/results-and-academic-statements/wam#:~:text=It%20is%20calculated%20progressively%20as,subject%20in%20calculating%20your%20WAM.) for more details.")
st.sidebar.latex(r"\sum_{i=1}^{n} \frac{c_i}{c_{tot}} \times g_i")
st.sidebar.markdown(
    "Where `n` is the number of subjects you have completed so far, `c_i` is the credit points for subject `i`, and `g_i` is the grade for subject `i`.")
st.sidebar.markdown("\n\n")
st.sidebar.markdown('---')

st.sidebar.write("☞ This site is fully **anonymous, secure and self contained**")
st.sidebar.markdown("☞ [Feature request/bug form](https://forms.gle/fHL4pfrdrjcWZeVVA)")

st.sidebar.markdown("\n\n")
st.sidebar.markdown('---')
st.sidebar.markdown('[Justin Lee 🐯]()')

col1, col2 = st.columns(2)


def render_grades():
    """ Render grade and credit points inputs """
    for i, grade_info in enumerate(st.session_state['grades']):
        with col1:
            if grade_info['grade'] == 0:
                st.text_input(f'Subject {i + 1}', value='Pass/Fail', key=f'grade_{i}')
            else:
                st.session_state['grades'][i]['grade'] = st.number_input(f'Subject {i + 1}', value=grade_info['grade'],
                                                                         key=f'grade_{i}', min_value=0, max_value=100)
        with col2:
            st.session_state['grades'][i]['credit_points'] = st.number_input(f'Credit Points',
                                                                             value=grade_info['credit_points'],
                                                                             key=f'credit_{i}')


render_grades()


def add_grade():
    st.session_state.grades.append({'grade': 50, 'credit_points': 12.5})


def remove_grade():
    if len(st.session_state.grades) > 1:
        st.session_state.grades.pop()


def add_passfail_grade():
    st.session_state.grades.append({'grade': 0, 'credit_points': 12.5})


with st.container():
    add_button, remove_button, passfail_button = st.columns([1, 1, 1])

    with add_button:
        add_button = st.button('Add Subject', on_click=add_grade)

    with remove_button:
        remove_button = st.button('Add Pass/Fail Subject', on_click=add_passfail_grade)

    with passfail_button:
        passfail_button = st.button('Remove Subject', on_click=remove_grade)

if not st.session_state.grades:
    st.markdown(f"### Your current WAM: **`{0.000:.3f}`**")
else:
    wam, tot_credit = calculate_wam(st.session_state.grades)
    st.markdown(f'**Total credit points:** `{tot_credit}`')
    st.markdown(f"### Your current WAM is **`{wam:.3f}`**")

st.markdown("---")

st.write('### More tools')


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
    st.session_state.upload_widget = True

if st.session_state.upload_widget:
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
        st.image('demo4.gif')


# CALCULATE GRADES NEEDED FOR DESIRED WAM
def slider_app(current_wam, num_completed):
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


num_completed = len(st.session_state.grades)
if st.button('Calculate grades needed for desired WAM'):
    if num_completed:
        st.session_state.button_pressed = True
    else:
        st.write('Please add at least one subject first')

if st.session_state.button_pressed:
    current_wam, _ = calculate_wam(st.session_state.grades)
    slider_app(current_wam, num_completed)

# STATS FOR NERDS
if st.button('Stats for Nerds'):
    if not num_completed:
        st.write('Please add at least one subject first')
    else:
        render_all_graphs(st.session_state.grades)
