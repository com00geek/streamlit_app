import os
import requests
import streamlit as st

# Load Hugging Face API token from secrets
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    st.error("Missing HF_TOKEN. Please add it in Streamlit Secrets.")
    st.stop()

# Model endpoint (replace with another mental health model if needed)
API_URL = "https://api-inference.huggingface.co/models/jondurbin/airoboros-2.2-mh"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_hf(prompt):
    payload = {
        "inputs": f"You are a compassionate mental health counselor.\nUser: {prompt}\nCounselor:",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            # Extract counselor part only
            return data[0]["generated_text"].split("Counselor:")[-1].strip()
        elif "error" in data:
            return f"API Error: {data['error']}"
        return str(data)
    except Exception as e:
        return f"Request failed: {e}"

# Streamlit UI
st.set_page_config(page_title="CalmMind AI", page_icon="🧘‍♂️")
st.title("🧘 CalmMind AI – Mental Wellness Chatbot")
st.markdown("A compassionate AI counselor fine-tuned for **mental health support**. Not a substitute for professional help.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_area("You:", placeholder="How are you feeling today?")

if st.button("Send"):
    if user_input.strip():
        st.session_state.chat_history.append(("You", user_input))
        bot_reply = query_hf(user_input)
        st.session_state.chat_history.append(("Counselor", bot_reply))

# Display chat history
for role, text in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Counselor:** {text}")

st.markdown("---")
st.caption("Disclaimer: This is a demo AI companion. If you are in crisis, please contact a mental health professional.")
