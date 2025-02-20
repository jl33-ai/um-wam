import streamlit as st


def render_sidebar():
    st.sidebar.markdown("### What is WAM?")
    st.sidebar.markdown(
        "Your WAM will be the average of the actual marks you achieved in all units of your course and is a mark out of 100.")
    st.sidebar.markdown(
        "The below WAM calculator is used to measure academic performance and can be used to determine eligibility for scholarships and honors programs.")

    st.sidebar.markdown('---')

    st.sidebar.markdown("### How to use this WAM calculator")
    st.sidebar.markdown(
        "1. Simply enter your marks for each subject by clicking 'Add Subject'")
    st.sidebar.markdown(
        "2. Optionally, click 'Autofill from Screenshot' to upload a screenshot of your grades")

    st.sidebar.markdown('---')

    st.sidebar.markdown("### How your WAM is calculated")
    st.sidebar.latex(r"\sum_{i=1}^{n} \frac{c_i}{c_{tot}} \times g_i")
    st.sidebar.markdown("""
        - `n` is the number of subjects you have completed so far
        - `c_i` is the credit points for subject `i`
        - `g_i` is the grade for subject `i`
        """)

    st.sidebar.markdown('---')

    st.sidebar.markdown("### Difference between WAM vs GPA")
    st.sidebar.markdown("""
        While WAM (Weighted Average Mark) and GPA (Grade Point Average) both measure academic performance,
        they differ in calculation methods. WAM uses percentage marks and credit points, making it the preferred
        system in Australian universities.""")
    st.sidebar.markdown("""GPA uses a 4.0 or 7.0 scale and is more common in American institutions.
        Our calculator focuses on the WAM system for accurate Australian university grade calculations.""")
    st.sidebar.markdown('---')

    st.sidebar.markdown("### About")
    st.sidebar.markdown("No data is stored or saved. This site is anonymous.")
    st.sidebar.markdown(
        "This site is no way affiliated with the University of Melbourne. See the [official university website](https://students.unimelb.edu.au/your-course/manage-your-course/exams-assessments-and-results/results-and-academic-statements/wam#:~:text=It%20is%20calculated%20progressively%20as,subject%20in%20calculating%20your%20WAM.) for more details.")

    st.sidebar.markdown('---')

    st.sidebar.markdown("### More")
    st.sidebar.markdown("[Suggest improvements or report issues](https://github.com/jl33-ai/um-wam/issues/new)")
    st.sidebar.markdown(
        "[Contribute to the source code](https://github.com/jl33-ai/um-wam/blob/main/docs/contributing.md)")
    st.sidebar.markdown('[Made by Justin](https://jl33-ai.github.io/)')
