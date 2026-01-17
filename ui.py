import streamlit as st
import requests

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="🧠",
    layout="centered"
)

st.markdown("<h1 style='text-align:center;'>🧠 AI Text Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Powered by your fine-tuned Pegasus model</p>", unsafe_allow_html=True)

# =========================
# Text Input
# =========================
text = st.text_area("Enter your text:", height=260)

# =========================
# Retrain Button
# =========================
if st.button("🔁 Retrain Model"):
    with st.spinner("Retraining model... this may take several minutes"):
        r = requests.get("http://127.0.0.1:8000/train")
        st.success(r.text)

# =========================
# Summarization UI
# =========================
if text.strip():

    word_count = len(text.split())

    # Dynamic summary bounds
    min_summary = max(30, word_count // 10)
    max_summary = max(80, word_count // 2)

    MAX_ALLOWED = 250
    max_summary = min(max_summary, MAX_ALLOWED)

    # Safety: ensure slider range is valid
    if min_summary >= max_summary:
        max_summary = min_summary + 1

    default_value = min((min_summary + max_summary) // 2, max_summary)

    target_words = st.slider(
        "Summary Length (words)",
        min_value=min_summary,
        max_value=max_summary,
        value=default_value
    )

    if st.button("✨ Generate Summary"):
        with st.spinner("Summarizing..."):
            response = requests.get(
                "http://127.0.0.1:8000/predict",
                params={
                    "text": text,
                    "max_length": target_words
                }
            )

            result = response.json()

            if "summary" in result:
                summary = result["summary"]

                st.success("Summary Generated")
                st.text_area("Summary", summary, height=200)

                actual_words = len(summary.split())
                compression = round(actual_words / word_count * 100, 1)

                st.caption(f"Output words: {actual_words} | Compression: {compression}%")
            else:
                st.error(result.get("error", "Unknown error"))
