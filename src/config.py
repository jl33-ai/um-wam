import streamlit as st


def get_secret(key):
    return st.secrets[key]


MAX_FILE_SIZE_MB = 5 * 1024 * 1024  # 5MB
