import streamlit as st


def render_sidebar():
    st.sidebar.markdown("### How your WAM is calculated")
    st.sidebar.latex(r"\sum_{i=1}^{n} \frac{c_i}{c_{tot}} \times g_i")
    st.sidebar.markdown("""
    - `n` is the number of subjects you have completed so far
    - `c_i` is the credit points for subject `i`
    - `g_i` is the grade for subject `i`
    """)
    st.sidebar.markdown("\n\n")
    st.sidebar.markdown('---')
    st.sidebar.write("This site is completely anonymous and secure.")
    st.sidebar.write(
        "This site is no way affiliated with the University of Melbourne. See the [official university website](https://students.unimelb.edu.au/your-course/manage-your-course/exams-assessments-and-results/results-and-academic-statements/wam#:~:text=It%20is%20calculated%20progressively%20as,subject%20in%20calculating%20your%20WAM.) for more details.")
    st.sidebar.markdown("[Feature request & Bug form](https://forms.gle/fHL4pfrdrjcWZeVVA)")
    st.sidebar.markdown('[Made by Justin](https://jl33-ai.github.io/)')
