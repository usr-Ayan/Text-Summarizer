import streamlit as st
import requests

st.set_page_config("AI Text Summarizer", "🧠", layout="centered")

st.markdown("<h1 style='text-align:center;'>🧠 AI Text Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Powered by your fine-tuned Pegasus model</p>", unsafe_allow_html=True)

# Text input
text = st.text_area("Enter your text:", height=260)

# Always visible retrain button
if st.button("🔁 Retrain Model"):
    with st.spinner("Retraining model... this may take several minutes"):
        r = requests.get("http://127.0.0.1:8000/train")
        st.success(r.text)

# Only show summarization controls when text is provided
if text:

    word_count = len(text.split())

    min_summary = max(30, word_count // 10)
    max_summary = max(80, word_count // 2)

    target_words = st.slider(
        "Summary Length (words)",
        min_value=min_summary,
        max_value=max_summary,
        value=(min_summary + max_summary) // 2
    )

    if st.button("✨ Generate Summary"):
        with st.spinner("Summarizing..."):
            response = requests.get(
                "http://127.0.0.1:8000/predict",
                params={"text": text, "max_length": target_words}
            )
            result = response.json()

            if "summary" in result:
                summary = result["summary"]
                st.success("Summary Generated")

                st.text_area("Summary", summary, height=200)

                actual_words = len(summary.split())
                st.caption(f"Output words: {actual_words} | Compression: {round(actual_words / word_count * 100, 1)}%")
            else:
                st.error(result.get("error", "Unknown error"))
