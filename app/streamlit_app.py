import os
import streamlit as st
from dotenv import load_dotenv

import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from app.config import (
    DEFAULT_CHUNK_SIZE,
    DEFAULT_TOP_K,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
)

from app.state import init_state
from core.crawler import crawl_url_sync
from core.chunking import split_markdown_into_chunks
from core.retrieval import rank_chunks, build_context_block
from core.prompts import system_prompt, user_prompt
from llm.ociLLM_client import ociLLMClient
from utils.text import safe_truncate

load_dotenv()
init_state()

st.set_page_config(page_title="DocAgent", layout="wide")
st.title("DocAgent")
st.caption("Crawl a website, extract content, and ask questions  compatible LLM.")

with st.sidebar:
    st.header("Crawler")
    site_name = st.text_input("Website name", value="Oracle Docs")
    site_input = st.text_input(
        "Website URL",
        value="https://docs.oracle.com/cd/F25688_01/xml_guide/Content/introduction/index.htm",
    )
    chunk_size = st.slider("Chunk size", 800, 3500, DEFAULT_CHUNK_SIZE, 100)
    top_k = st.slider("Top chunks", 2, 10, DEFAULT_TOP_K)

    st.header("LLM")
    provider = st.selectbox("Provider", ["openai", "ollama"], index=0)
    api_key = st.text_input("API key", value=os.getenv("OPENAI_API_KEY", ""), type="password")
    base_url = st.text_input(
        "Base URL",
        value=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )
    model = st.text_input("Model", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    temperature = st.slider("Temperature", 0.0, 1.0, DEFAULT_TEMPERATURE, 0.05)
    max_tokens = st.slider("Max tokens", 256, 4000, DEFAULT_MAX_TOKENS, 64)

    show_raw = st.checkbox("Show raw markdown", value=False)
    show_chunks = st.checkbox("Show selected chunks", value=True)

question = st.text_area(
    "Ask a question about the website",
    value="What is this page about?",
    height=120,
)

col1, col2 = st.columns(2)
crawl_clicked = col1.button("Crawl website", type="primary")
answer_clicked = col2.button("Answer question")

if crawl_clicked:
    st.session_state.crawl_error = ""
    st.session_state.last_answer = ""

    with st.spinner("Crawling website..."):
        try:
            markdown = crawl_url_sync(site_input)
            if not markdown.strip():
                raise RuntimeError("Crawler returned empty content.")

            st.session_state.markdown = markdown
            st.session_state.chunks = split_markdown_into_chunks(markdown, max_chars=chunk_size)
            st.session_state.last_url = site_input
            st.success(f"Crawled successfully. Extracted {len(st.session_state.chunks)} chunks.")
        except Exception as exc:
            st.session_state.crawl_error = str(exc)
            st.error(f"Failed to crawl: {exc}")

if st.session_state.crawl_error:
    st.warning(st.session_state.crawl_error)

if answer_clicked:
    if not st.session_state.markdown.strip():
        st.error("Please crawl a website first.")
    elif not question.strip():
        st.error("Please enter a question.")
    # elif not api_key.strip() and provider != "ollama":
    #     st.error("Please provide an API key.")
    else:
        llm = ociLLMClient()

        selected = rank_chunks(question, st.session_state.chunks, top_k=top_k)
        st.session_state.selected_chunks = selected
        context = build_context_block(selected)

        with st.spinner("Thinking..."):
            answer = llm.chat(
                system_prompt=system_prompt(),
                user_prompt=user_prompt(
                    question=question,
                    site_name=site_name,
                    site_url=site_input,
                    context=context,
                ),
            )
            st.session_state.last_answer = answer

if st.session_state.last_answer:
    st.subheader("Answer")
    st.write(st.session_state.last_answer)

if show_chunks and st.session_state.selected_chunks:
    with st.expander("Selected chunks", expanded=True):
        for chunk in st.session_state.selected_chunks:
            st.markdown(f"**Chunk {chunk.chunk_id}**  ")
            st.caption(f"Score: {chunk.score:.3f}")
            st.code(safe_truncate(chunk.text, 6000))

if show_raw and st.session_state.markdown.strip():
    with st.expander("Raw crawled markdown"):
        st.code(safe_truncate(st.session_state.markdown, 20000))