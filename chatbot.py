import streamlit as st
from google import genai
from google.genai import types

# Page configs
st.set_page_config(page_title="Procurement AI Assistant", page_icon="📦", layout="centered")
st.title("📦 Procurement & Sourcing AI Assistant")
st.caption("Powered by a live Gemini AI Model")

# 1. Initialize the Google GenAI Client
# It will read the API key securely from your st.secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Define the System Persona instructions for the AI
SYSTEM_PROMPT = """
You are an expert Corporate Procurement and Supply Chain Specialist. Your role is to assist users with:
1. Drafting Request for Proposals (RFPs), RFQs, and RFIs.
2. Formulating vendor evaluation frameworks and weighted scoring sheets.
3. Providing advice on contract negotiation tactics and mitigation of supply chain risks.
4. Explaining procurement core concepts (e.g., TCO, Incoterms, SLA metrics).
Always maintain a professional, risk-aware, and compliance-driven tone. If asked about things completely unrelated to procurement, gently steer the conversation back.
"""

# 3. Initialize Conversation History in Streamlit Memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your live AI procurement assistant. Ask me anything about RFPs, supplier evaluation, or supply chain risk!"}
    ]

# 4. Render existing chat logs on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Capture User Input
if prompt := st.chat_input("Ask a procurement question..."):
    
    # Display what the user typed
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 6. Call the Live Gemini AI and Stream the response
    with st.chat_message("assistant"):
        
        # Format our Streamlit chat history into the structure Gemini expects
        gemini_history = []
        for msg in st.session_state.messages[:-1]: # exclude the brand new prompt
            # Map roles to what Gemini expects ('user' or 'model')
            g_role = "user" if msg["role"] == "user" else "model"
            gemini_history.append(types.Content(role=g_role, parts=[types.Part.from_text(text=msg["content"])]))

        # Generate a live content stream
        response_stream = client.models.generate_content_stream(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT, # Forces the AI to stay in character
                temperature=0.7
            )
        )
        
        # Create a helper function so st.write_stream can animate the text
        def stream_chunks():
            for chunk in response_stream:
                yield chunk.text

        # Animate the live response directly onto the web interface
        full_response = st.write_stream(stream_chunks())
        
    # Save the AI's real response to memory
    st.session_state.messages.append({"role": "assistant", "content": full_response})
