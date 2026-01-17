import streamlit as st
import google.generativeai as genai

# 1. API Configuration
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# 2. Hidden System Prompts (The "Patients")
PATIENT_PROMPTS = {
    "Level 1: Sami (Sore Throat)": "You are Sami, an 18-year-old student with a sore throat. Act cooperative. Don't reveal your diagnosis. Only tell the student you feel 'burning' when swallowing. Wait for them to ask questions.",
    "Level 2: Mrs. Layla (Chronic Cough)": "You are Mrs. Layla. You have a cough that's worse at night. Be slightly frustrated. Only mention your sour taste in the mouth if they ask about digestion.",
    "Level 3: Abu Mazen (Chest Pain)": "You are Abu Mazen, 62. You have crushing chest pain. You are stoic and scared. Don't volunteer info easily. Act like a real patient in distress."
}

# 3. UI Setup
st.set_page_config(page_title="JUST SCOME: Medical Sim", page_icon="🩺")
st.title("🩺 Clinical History Simulator")
st.sidebar.title("Select Case")
selected_case = st.sidebar.selectbox("Choose a patient level:", list(PATIENT_PROMPTS.keys()))

# 4. Initialize Chat Session
if "messages" not in st.session_state or st.sidebar.button("Reset Simulation"):
    st.session_state.messages = []
    # Set the hidden system prompt
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-flash-latest",
        system_instruction=PATIENT_PROMPTS[selected_case]
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input
if prompt := st.chat_input("Start your history taking..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI Response
    response = st.session_state.chat.send_message(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})