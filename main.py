import streamlit as st
from streamlit_echarts import st_echarts

import requests
from io import BytesIO
import re

st.set_page_config(page_title="University WAM Calculator")

st.write("## Calculate your Weighted Average Mark (WAM)")


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Define your OCR.space API key here
API_KEY = 'K85283192788957'

def ocr_space_file(file_stream, api_key, language='eng'):
    """ OCR.space API request with file stream. """
    payload = {
        'apikey': api_key,
        'language': language,
    }
    response = requests.post(
        'https://api.ocr.space/parse/image',
        files={file_stream.name: file_stream},
        data=payload,
    )
    return response.json()

def to_list(grade_str):
    """ Uses regex to find all numbers in the OCR result string. """
    return re.findall(r'\d+', grade_str)

def populate_grades(grade_list):
    """ Clears the current list and populates it with new grades. """
    st.session_state.grades.clear()
    for _, grade in enumerate(grade_list):
        st.session_state.grades.append({'grade': int(grade), 'credit_points': 12.5})
    if 'upload_widget' in st.session_state:
        st.session_state.upload_widget = False
    st.experimental_rerun()

def extract_grades(my_upload):
    """ Extracts grades from columnar screenshot and populates the table. """
    if my_upload is not None:
        if my_upload.size > MAX_FILE_SIZE:
            st.error("The uploaded screenshot is too large. Please upload an image smaller than 5MB.")
        else:
            # Perform OCR using OCR.space API
            ocr_result = ocr_space_file(my_upload, API_KEY)
            ocr_text = ocr_result.get('ParsedResults')[0].get('ParsedText')

            # REGEX step to extract grades
            grade_list = to_list(ocr_text)

            # Populate the grades
            populate_grades(grade_list)

# Intialise session states

if 'grades' not in st.session_state:
    st.session_state.grades = [{'grade': 50, 'credit_points': 12.5}]

if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = False

if 'upload_widget' not in st.session_state:
    st.session_state.upload_widget = False


st.sidebar.markdown("### How your WAM is calculated")
st.sidebar.markdown("See the official [University of Melbourne website](https://students.unimelb.edu.au/your-course/manage-your-course/exams-assessments-and-results/results-and-academic-statements/wam#:~:text=It%20is%20calculated%20progressively%20as,subject%20in%20calculating%20your%20WAM.) for more details.")
st.sidebar.latex(r"\sum_{i=1}^{n} \frac{c_i}{c_{tot}} \times g_i")
st.sidebar.markdown("Where `n` is the number of subjects you have completed so far, `c_i` is the credit points for subject `i`, and `g_i` is the grade for subject `i`.")
st.sidebar.markdown("\n\n")
st.sidebar.markdown('---')

st.sidebar.write("☞ This site is fully **anonymous, secure and self contained**")
st.sidebar.markdown("☞ [Feature request/bug form](https://forms.gle/fHL4pfrdrjcWZeVVA)")


st.sidebar.markdown("\n\n")
st.sidebar.markdown('---')
st.sidebar.markdown('[UM-WC v1.0.1]() | Nov 2023')
st.sidebar.markdown('[Justin Lee 🐯]()')


col1, col2 = st.columns(2)

# dynamically display the grade and credit points inputs
for i, grade_info in enumerate(st.session_state['grades']):
    with col1:
        # Create a number input for grade, unique key is necessary for each input
        if grade_info['grade'] == 0: 
            st.text_input(f'Subject {i+1}', value='Pass/Fail', key=f'grade_{i}')
        else: 
            st.session_state['grades'][i]['grade'] = st.number_input(f'Subject {i+1}', value=grade_info['grade'], key=f'grade_{i}', min_value=0, max_value=100)
    with col2:
        # Create a number input for credit points, unique key is necessary for each input
        st.session_state['grades'][i]['credit_points'] = st.number_input(f'Credit Points', value=grade_info['credit_points'], key=f'credit_{i}')

# display the current state of grades (debug)
# st.write('Current Grades:', st.session_state['grades'])

ucol1, ucol2 = st.columns([1, 2])

# function to add a grade entry
def add_grade():
    st.session_state.grades.append({'grade': 50, 'credit_points': 12.5})

def remove_grade():
    if len(st.session_state.grades) > 1:
        st.session_state.grades.pop()

def add_passfail():
    st.session_state.grades.append({'grade': 0, 'credit_points': 12.5})
    


with st.container():
    # Create a horizontal layout
    add_button, remove_button, passfail_button = st.columns([1, 1, 1])

    # Place each button in its respective column
    with add_button:
        add_button = st.button('Add Subject', on_click=add_grade)

    with remove_button:
        remove_button = st.button('Add Pass/Fail Subject', on_click=add_passfail)

    with passfail_button:
        passfail_button = st.button('Remove Subject', on_click=remove_grade)
        
#add_button = st.button(' Add Subject  ', on_click=add_grade)
#remove_button = st.button('Remove Subject', on_click=remove_grade)
#passfail_button = st.button('Add Pass/Fail Subject', on_click=add_passfail)


def calculate_wam(grades):
    tot_credit = sum(g['credit_points'] for g in grades)
    all_credit = sum(g['credit_points'] for g in grades if g['grade'] > 0)
    wam = sum([g['grade']*(g['credit_points']/all_credit) for g in grades]) if grades else 0
    return wam, tot_credit

if not st.session_state.grades: 
    st.markdown(f"### Your current WAM: **`{0.000:.3f}`**")
else: 
    wam, tot_credit = calculate_wam(st.session_state.grades)
    st.markdown(f"### Your current WAM: **`{wam:.3f}`**")
    st.write(f'**Total credit points:** `{tot_credit}`')

st.markdown("---")



# EXTRAS 

st.write('## More tools:')
#st.write('🧪🧮📊🎰📷')

def slider_app(current_wam, num_completed):
    desired_wam = st.slider("Desired WAM", 50, 100, 75)
    remaining_subjects = st.number_input("Number of Remaining Subjects (You may go above 24)", min_value=1, value=(24-num_completed))
    if remaining_subjects > 0:
        total_subjects = num_completed + remaining_subjects
        required_average = ((desired_wam * total_subjects) - (current_wam * num_completed)) / remaining_subjects
        st.markdown(f"### Average score needed to achieve a WAM of {desired_wam}: **`{required_average:.2f}`**")
    else:
        st.write("Please enter the number of completed subjects and remaining subjects.")

    st.markdown("---") #sexy+code(R) -

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
    elif g == 0:
        return '*'
    else:
        return 'N'

def calculate_stats(grades):
    freq_dict = {'H1' : 0, 'H2A' : 0, 'H2B' : 0, 'H3' : 0, 'P' : 0, 'N' : 0, '*' : 0}
    maximum_g = 0
    minimum_g = 100

    for g in grades:
        freq_dict[get_grade(g['grade'])] += 1
        if g['grade'] > maximum_g:
            maximum_g = g['grade']
        if g['grade'] < minimum_g:
            minimum_g = g['grade']


    return freq_dict, maximum_g, minimum_g


    
def plot_progression():
    return






# Statistics, Plot, Slider, Radar Map, Comments, H1 Pie
# Subjects remaining in course: (default 24 subejcts)
# To obtain a wam of (number)
# You need to maintain an average of: in your remaining subjects 



# Button to reveal the slider
num_completed = len(st.session_state.grades)
if st.button('Calculate grades needed for desired WAM'):
    if num_completed:
        st.session_state.button_pressed = True
    else: 
        st.write('Please add at least one subject first')

# Check if the button has been pressed
if st.session_state.button_pressed:
    current_wam, _ = calculate_wam(st.session_state.grades) # Replace with your actual function to calculate WAM
    slider_app(current_wam, num_completed)
        


def render_basic_radar(grades):
    data, gmax, gmin = calculate_stats(grades)  # Replace with your actual function
    g_data = []
    maximum = 0

    # Use Streamlit's columns to place text and graph side by side
    col1, col2 = st.columns([1, 2])  # Adjust the ratio as needed

    with col1:
        st.markdown('#### So far, you have achieved:')
        for g, f in data.items(): 
            if f: 
                st.markdown(f"##### `{int(f)}` {g.upper()}'s")
                if f > maximum: 
                    maximum = f
            g_data.append(int(f))
        st.markdown('#### Your best grade:')
        st.markdown(f'##### `{gmax}`')
        st.markdown('#### Your lowest grade:')
        st.markdown(f'##### `{gmin}`')
        st.markdown("*Don't worry, it happens :)*")

    with col2:
        option = {
            "title": {
                "textStyle": {"fontSize": 16, "fontWeight": "bold"},
                "left": "center"
            },
            
            "radar": {
                "indicator": [
                    {"name": "H1", "max": maximum},
                    {"name": "H2A", "max": maximum},
                    {"name": "H2B", "max": maximum},
                    {"name": "H3", "max": maximum},
                    {"name": "P", "max": maximum},
                    {"name": "N", "max": maximum},
                    {"name": "*", "max": maximum}
                ],
                "splitNumber": 5
            },
            "series": [
                {
                    "name": "Data",
                    "type": "radar",
                    "data": [
                        {
                            "value": g_data,
                            "name": "Grades by Title",
                            "areaStyle": {"color": "#87d068"}
                        }
                    ],
                }
            ],
        }
        st_echarts(option, height="500px")

    render_basic_area_chart(grades)
    #st.markdown('---')


def render_basic_area_chart(grades):
    data = []
    for i in range(len(grades)):
        wam, _ = calculate_wam(grades[:i+1])
        data.append(int(wam))


    # Determine the min and max values for the y-axis
    min_value = min(data) - 5
    max_value = max(data) + 5

    options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "cross",
                "label": {"backgroundColor": "#6a7985"}
            }
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": [str(i+1) for i in range(len(grades))]  # assuming each grade corresponds to a subject number
        },
        "yAxis": {
            "type": "value",
            "min": min_value,
            "max": max_value
        },
        "series": [
            {
                "data": data,
                "type": "line",
                "smooth": True,  # Makes the line smooth
                "symbol": "none",  # Hides the symbols on the line
                "areaStyle": {
                    "color": "rgba(135, 208, 104, 0.6)",  # Adjust color and transparency
                },
                "lineStyle": {
                    "color": "rgba(135, 208, 104, 1)",
                    "width": 2
                },
                "itemStyle": {
                    "color": "rgba(135, 208, 104, 1)"
                }
            }
        ],
    }
    st.write('### Your WAM over time')
    st_echarts(options=options, height="500px")
    st.markdown('---')


if st.button('Stats for Nerds'):
    if not num_completed:
        st.write('Please add at least one subject first')
    else:
        render_basic_radar(st.session_state.grades)

#if st.button('View WAM over Time'):
#    if not num_completed:
#        st.write('Please add at least one subject first')
#    else:
#        render_basic_area_chart(st.session_state.grades)
    
    

def autofill_callback():
    extract_grades(my_upload)



if st.button('Autofill from Screenshot'):
    st.session_state.upload_widget = True
    
if st.session_state.upload_widget:
    my_upload = st.file_uploader("📄 Upload a screenshot of ONLY your grades column", type=["png", "jpg", "jpeg"])
    st.markdown('---')
    mcol1, mcol2 = st.columns([1, 2])
    if st.button('Autofill'):
        if my_upload:
            autofill_callback()
        else:
            st.write('Please upload a correct file first')
    with mcol1:
        st.write('#### How to submit')
        st.write("☞ Never include **subject codes** or your **studentID**")
        st.write("☞ Your screenshot should include only the 'marks' column as shown")
        st.write("☞ Warning: Autofilling will **overwrite all current grades**")
    with mcol2:
        st.image('demo4.gif')
    

    st.markdown('---')


if st.button('Exam Weighting Calculator'):
    st.write('Work in Progress...')
    st.markdown('---')

# Leave a comment!
