import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="MSU-GenSan Procurement Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# Custom CSS for MSU-GenSan Theme
# ------------------------------
st.markdown(
    """
    <style>
    /* MSU Maroon & Gold Theme */
    :root {
        --msu-maroon: #800000;
        --msu-gold: #FFD700;
        --msu-dark-maroon: #5a0000;
        --light-bg: #fef9e6;
    }
    
    .stApp {
        background-color: var(--light-bg);
    }
    
    h1, h2, h3 {
        color: var(--msu-maroon);
        font-family: 'Georgia', serif;
    }
    
    .stChatMessage {
        border-radius: 20px;
        padding: 10px 15px;
        margin-bottom: 10px;
    }
    
    [data-testid="stChatMessage"][aria-label="user"] {
        background-color: #e6e6fa;
    }
    
    [data-testid="stChatMessage"][aria-label="assistant"] {
        background-color: #fff3e0;
        border-left: 5px solid var(--msu-maroon);
    }
    
    .sidebar-content {
        background-color: #fff0d4;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .msu-logo-text {
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        color: var(--msu-maroon);
        border-bottom: 2px solid var(--msu-gold);
        margin-bottom: 15px;
    }
    
    .badge {
        background-color: var(--msu-maroon);
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        display: inline-block;
    }
    
    .footer {
        font-size: 0.75rem;
        text-align: center;
        color: gray;
        margin-top: 30px;
        border-top: 1px solid #ddd;
        padding-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Sidebar – MSU-GenSan Info & Tools
# ------------------------------
with st.sidebar:
    st.markdown('<div class="msu-logo-text">🏛️ MSU-GenSan<br>Procurement Hub</div>', unsafe_allow_html=True)
    st.caption("Republic Act 9184 Compliant")
    
    st.markdown("---")
    st.subheader("📌 Quick Tools")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared. How can I assist with MSU procurement today?"}
        ]
        st.rerun()
    
    st.markdown("---")
    st.subheader("📚 University Context")
    st.info(
        "This assistant is fine-tuned for **Mindanao State University - General Santos** "
        "procurement processes, including:\n\n"
        "- RA 9184 (Government Procurement Reform Act)\n"
        "- BAC (Bids and Awards Committee) procedures\n"
        "- Small Value Procurement (SVP)\n"
        "- Shopping & Negotiated Procurement\n"
        "- University supplier accreditation\n\n"
        "*For official transactions, consult the MSU-GenSan BAC office.*"
    )
    
    st.markdown("---")
    st.subheader("💡 Example Prompts")
    st.markdown(
        """
        - Draft an RFP for IT equipment (50 laptops) for MSU-GenSan.
        - How do I compute the ABC (Approved Budget for the Contract) under RA 9184?
        - Create a weighted scoring matrix for janitorial services bid.
        - Explain Incoterms 2024 for international lab equipment.
        - What are common supply chain risks in SOCCSKSARGEN region?
        """
    )
    
    st.markdown("---")
    st.markdown(
        '<div class="footer">Powered by Gemini 2.5 Flash<br>© 2025 MSU-GenSan Procurement Office</div>',
        unsafe_allow_html=True
    )

# ------------------------------
# Main Chat Interface
# ------------------------------
st.title("📦 MSU-GenSan Procurement & Sourcing AI")
st.caption("Your AI procurement specialist – trained on Philippine government procurement rules and MSU policies.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Magandang araw! I am your MSU-GenSan procurement assistant. Ask me about RA 9184, RFPs, supplier evaluation, or supply chain risk management for the university."}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------
# Gemini API Client
# ------------------------------
@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

# Enhanced system prompt with MSU-GenSan context
SYSTEM_PROMPT = f"""
You are an expert Corporate Procurement and Supply Chain Specialist for **Mindanao State University - General Santos (MSU-GenSan)**.
Your role is to assist faculty, staff, and BAC members with public procurement in the Philippines, strictly following RA 9184 and its IRR.

Key university context:
- MSU-GenSan is a state university in South Cotabato, SOCCSKSARGEN region.
- Procurement follows Government Procurement Reform Act (RA 9184).
- Common modes: Public Bidding, Limited Source Bidding, Negotiated Procurement, Small Value Procurement (up to ₱1M per item), and Shopping (₱50k - ₱500k depending on goods).
- BAC (Bids and Awards Committee) oversees the process.
- Philippine Transparency and accountability requirements (PhilGEPS posting, BAC resolutions).

Your capabilities:
1. **Drafting** RFPs, RFQs, RFIs, and BAC resolutions.
2. **Vendor evaluation** – weighted scoring sheets (criteria: price, technical capability, delivery, after-sales).
3. **Contract negotiation tactics** and risk mitigation (force majeure, penalties, warranties).
4. **Explaining concepts** – TCO, Incoterms 2024, SLAs, performance security, liquidated damages.
5. **Compliance checks** – ensuring procurement aligns with RA 9184, COA rules, and university guidelines.

Always maintain a professional, risk-aware, compliance-driven tone. If asked about unrelated topics (e.g., politics, entertainment), gently steer back to procurement. When referencing amounts, use Philippine Peso (₱). Cite relevant sections of RA 9184 when helpful.
Current date: {datetime.now().strftime("%B %d, %Y")}
"""

# ------------------------------
# Handle User Input & Stream Response
# ------------------------------
if prompt := st.chat_input("Ask a procurement question (e.g., 'Draft an RFP for library books')..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Build conversation history for Gemini
    gemini_history = []
    for msg in st.session_state.messages[:-1]:  # exclude the latest user message (we'll add it separately)
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append(types.Content(
            role=role,
            parts=[types.Part.from_text(text=msg["content"])]
        ))
    
    # Add current user prompt as last user content
    current_user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt)]
    )
    full_contents = gemini_history + [current_user_content]
    
    # Generate streaming response
    with st.chat_message("assistant"):
        try:
            response_stream = client.models.generate_content_stream(
                model='gemini-2.5-flash',
                contents=full_contents,  # send full conversation for context
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    top_p=0.95,
                )
            )
            
            def stream_chunks():
                for chunk in response_stream:
                    if chunk.text:
                        yield chunk.text
            
            full_response = st.write_stream(stream_chunks())
            
        except Exception as e:
            full_response = f"⚠️ Error connecting to AI service: {str(e)}. Please check your API key or network."
            st.error(full_response)
    
    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
