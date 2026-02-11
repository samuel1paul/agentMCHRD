import streamlit as st
from openai import OpenAI

# -------------------------------------------------
# APP CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Citizen Grievance Guidance Chatbot",
    layout="centered"
)

st.title("📝 Citizen Grievance Guidance Chatbot")
st.caption(
    "Provides procedural guidance only. "
    "Final decisions rest with the concerned Government authority."
)

# -------------------------------------------------
# API KEY CHECK
# -------------------------------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not configured.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------------------------------
# SYSTEM PROMPT (LOCKED)
# -------------------------------------------------
SYSTEM_PROMPT = """
You are a Citizen Grievance Guidance Assistant for a Government Department.

Provide only procedural and informational guidance related to grievance filing.

Rules:
- Do not judge or evaluate grievances.
- Do not provide legal advice.
- Do not promise outcomes.
- Do not resolve grievances.
- Redirect citizens to concerned authorities when needed.

Always include this disclaimer:
"This information is for guidance purposes only and does not constitute a decision or assurance by the Government."
"""

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I can guide you on how to file a grievance, "
                "required documents, timelines, and where to submit it.\n\n"
                "This information is for guidance purposes only and does not constitute a decision or assurance by the Government."
            )
        }
    ]

# -------------------------------------------------
# CHAT DISPLAY
# -------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Please wait..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.2,
                max_tokens=500,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages
                ]
            )

            reply = response.choices[0].message.content
            st.markdown(reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )
