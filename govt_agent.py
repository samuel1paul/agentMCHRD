import streamlit as st
from openai import OpenAI
from pypdf import PdfReader
import os

# ---------------------------------
# CONFIG
# ---------------------------------
# -------------------------------------------------
# API KEY CHECK
# -------------------------------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not configured.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------------------
# FIXED GOVT AGENT PROMPT (LOCKED)
# ---------------------------------
SYSTEM_PROMPT = """
ROLE:
You are an AI Assistant supporting a Government Officer.

RULES:
1. Use formal Government language.
2. Use only the information provided in the uploaded documents.
3. Do not assume or infer missing details.
4. If information is missing, state "Information not available in the provided documents".
5. Do not provide opinions or policy recommendations.

OUTPUT:
Respond in clear bullet points or numbered format suitable for official records and briefings.
"""

# ---------------------------------
# UI
# ---------------------------------
st.title("🧾 Government AI Assistant (Training)")
st.caption("AI-assisted drafting and summarization – Human decision remains final")

uploaded_file = st.file_uploader("Upload Government Document (PDF only)", type=["pdf"])
user_query = st.text_input("Enter instruction (e.g., 'Summarize for briefing')")

# ---------------------------------
# FILE READING
# ---------------------------------
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# ---------------------------------
# ACTION
# ---------------------------------
if st.button("Generate Response"):
    if not uploaded_file or not user_query:
        st.warning("Please upload a document and enter an instruction.")
    else:
        with st.spinner("Processing..."):
            document_text = extract_text_from_pdf(uploaded_file)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.2,
                max_tokens=900,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"DOCUMENT:\n{document_text}"},
                    {"role": "user", "content": user_query}
                ]
            )

            st.subheader("📌 AI Draft Output")
            st.write(response.choices[0].message.content)




