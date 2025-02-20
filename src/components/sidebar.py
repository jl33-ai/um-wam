import streamlit as st


def render_sidebar():
    st.sidebar.write("### About")
    st.sidebar.markdown(
        "This site is no way affiliated with the University of Melbourne. See the [official university website](https://students.unimelb.edu.au/your-course/manage-your-course/exams-assessments-and-results/results-and-academic-statements/wam#:~:text=It%20is%20calculated%20progressively%20as,subject%20in%20calculating%20your%20WAM.) for more details.")
    st.sidebar.markdown("No data is stored or saved. This site is anonymous.")
    st.sidebar.write("### More")
    st.sidebar.markdown("[Suggest improvements or report issues](https://github.com/jl33-ai/um-wam/issues/new)")
    st.sidebar.markdown(
        "[Contribute to the source code](https://github.com/jl33-ai/um-wam/blob/main/docs/contributing.md)")
    st.sidebar.markdown('[This site was built by Justin](https://jl33-ai.github.io/)')
