import streamlit as st

def init_state():
    defaults = {
        "markdown": "",
        "chunks": [],
        "selected_chunks": [],
        "last_answer": "",
        "last_url": "",
        "crawl_error": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_answer():
    st.session_state.last_answer = ""

def reset_crawl():
    st.session_state.markdown = ""
    st.session_state.chunks = []
    st.session_state.selected_chunks = []
    st.session_state.last_answer = ""
    st.session_state.last_url = ""
    st.session_state.crawl_error = ""