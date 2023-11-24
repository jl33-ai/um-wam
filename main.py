import streamlit as st
from io import BytesIO
from PIL import Image
import cv2
import pytesseract
import numpy as np
import re

st.set_page_config(layout="wide", page_title="UniMelb WAM Calculator")

st.write("## Calculate your Weighted Average Mark")


st.sidebar.write("## Autofill from Screenshot 📄")

# initialize a session state for grades
if 'grades' not in st.session_state:
    st.session_state.grades = []


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def preprocess(img):
    """
    Performs loading, conversion to np image array, greyscale, binary image, upscaling
    """
    image = Image.open(img).convert('RGB')
    image_nparray = np.array(image)
    gray_image = cv2.cvtColor(image_nparray, cv2.COLOR_RGB2GRAY)
    _, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #inverted_binary = cv2.bitwise_not(binary_image)
    resized_image = cv2.resize(binary_image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    return Image.fromarray(resized_image)
    
def to_list(grade_str):
    """
    Uses regex
    """
    return re.findall(r'\d+', grade_str)

def populate_grades(grade_list):
    """
    CLEARS CURRENT LISTE FIRST
    """
    st.session_state.grades.clear()
    for i, grade in enumerate(grade_list):
        st.session_state.grades.append({'grade': int(grade), 'credit_points': 12.5})

def extract_grades(my_upload):
    """
    Exracts grades from columnar screenshot and populates table
    """
    if my_upload is not None:
        if my_upload.size > MAX_FILE_SIZE:
            st.error("The uploaded screenshot is too large. Please upload an image smaller than 5MB.")
        else:
            # preprocess
            image = preprocess(my_upload)
    
             # Perform OCR
            ocr_result = pytesseract.image_to_string(image, config=r'--oem 3 --psm 6 outputbase digits')
            
            # REGEX step
            grade_list = to_list(ocr_result)

            # Print OCR output (for diagnostics)
            # st.text(grade_list)

            # now populates list
            populate_grades(grade_list)

my_upload = st.sidebar.file_uploader("Upload a screenshot of your grades:", type=["png", "jpg", "jpeg"])



st.sidebar.write("☞ Never include **subject codes** or your **studentID**")
st.sidebar.write('☞ **Warning**: this will clear all current grades')
st.sidebar.markdown("☞ I know we hate looking at our own WAM enough, let alone letting other people see. So I've made every effort to make this website **fully secure** and self contained.")

def autofill_callback():
    extract_grades(my_upload)

if st.sidebar.button('Autofill'):
    autofill_callback()

col1, col2 = st.columns(2)

# dynamically display the grade and credit points inputs
for i, grade_info in enumerate(st.session_state['grades']):
    with col1:
        # Create a number input for grade, unique key is necessary for each input
        st.session_state['grades'][i]['grade'] = st.number_input(f'Grade {i+1}', value=grade_info['grade'], key=f'grade_{i}')
    with col2:
        # Create a number input for credit points, unique key is necessary for each input
        st.session_state['grades'][i]['credit_points'] = st.number_input(f'Credit Points', value=grade_info['credit_points'], key=f'credit_{i}')

# display the current state of grades (debug)
# st.write('Current Grades:', st.session_state['grades'])

# function to add a grade entry
def add_grade():
    st.session_state.grades.append({'grade': 0, 'credit_points': 12.5})
    
# button to add a grade entry
st.button('Add Grade', on_click=add_grade)




st.write('## Results')

def calculate_wam(grades):
    if not grades:
        st.write('Please add some subject scores')
    else: 
        all_credit = sum(g['credit_points'] for g in grades)
        wam = sum([g['grade']*(g['credit_points']/all_credit) for g in grades]) if grades else 0
        st.write(f'Your WAM is: {round(wam, 3)}')

    return 


def get_grade(g):
    if g >= 80:
        return 'H1'
    elif g >= 75:
        return 'H2A'
    elif g >= 70:
        return 'H2B'
    elif g >= 65:
        return 'H3'
    elif g >= 50:
        return 'P'
    elif g == 49:
        return 'NH'
    else:
        return 'N'

def calculate_stats():
    freq_dict = {}
    for g in grades: 
        pass


calculate_wam(st.session_state.grades)


# Statistics, Plot, Slider, Radar Map, Comments, H1 Pie
# Subjects remaining in course: (default 24 subejcts)
# To obtain a wam of (number)
# You need to maintain an average of: in your remaining subjects 

st.markdown("---")  
st.markdown("### How Your WAM is Calculated")
st.markdown("See the official [University of Melbourne website](https://students.unimelb.edu.au/your-course/manage-your-course/exams-assessments-and-results/results-and-academic-statements/wam#:~:text=It%20is%20calculated%20progressively%20as,subject%20in%20calculating%20your%20WAM.) for more details.")
st.latex(r"\sum_{i=1}^{n} c_i \times g_i")
st.markdown("Where `n` is the number of subjects you have completed so far, `c_i` is the credit points for subject `i`, and `g_i` is the grade for subject `i`.")


# You can add additional information or decorative elements as needed.
# For example, a contact info section or a disclaimer.
