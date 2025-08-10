import streamlit as st
import requests

# --- Config ---
MODEL = "Skshackster/gemma3-1b-mental-health-fine-tuned"  # Public, therapy-focused
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

SYSTEM_PROMPT = (
    "You are a compassionate mental health counselor. Respond with empathy, warmth, and brief actionable support. "
    "Keep responses under 150 words."
)

# --- Streamlit UI ---
st.set_page_config(page_title="CalmMind AI (Mental Health Chatbot)", layout="centered")
st.title("🌿 CalmMind AI — Mental Health Chatbot (Demo)")
st.write("Not a replacement for therapy. If you're in crisis, seek professional help.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("How are you feeling today?")

def ask_hf(prompt):
    response = requests.post(API_URL, json={"inputs": prompt})
    if response.status_code != 200:
        return f"Error: {response.status_code}"
    return response.json()[0]["generated_text"]

if st.button("Send") and user_input:
    prompt = SYSTEM_PROMPT + "\n\n"
    for human, ai in st.session_state.history:
        prompt += f"User: {human}\nTherapist: {ai}\n"
    prompt += f"User: {user_input}\nTherapist:"
    reply = ask_hf(prompt).split("Therapist:")[-1].strip()[:800]
    st.session_state.history.append((user_input, reply))

for human, ai in st.session_state.history:
    st.markdown(f"**You:** {human}")
    st.markdown(f"**Counselor:** {ai}")
    st.markdown("---")

if st.button("Clear"):
    st.session_state.history = []
st.write("Chat history cleared.")