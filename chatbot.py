import streamlit as st
import time

# Page configuration matched to MSU / Isko BidDo theme
st.set_page_config(page_title="Isko BidDo AI Inquiry", page_icon="🤖", layout="centered")
st.title("🤖 Isko BidDo: AI Inquiry Support")
st.caption("Mindanao State University - General Santos City | Digital Procurement Assistant")

# 1. Define the Isko BidDo Knowledge Base & Persona
SYSTEM_PROMPT = """
You are the Isko BidDo AI Inquiry Support Assistant for Mindanao State University - General Santos (MSU-Gensan). 
Your system parameters are dictated by Philippine Public Procurement Laws: RA 9184 and its critical transition into RA 12009 (New Government Procurement Act - NGPA).

Your specialized tasks include helping MSU staff and the Bids and Awards Committee (BAC) with:
1. Explaining standard procurement workflows (PPMP, APP, Purchase Requests).
2. Clarifying legal requirements under RA 12009 (e.g., Mandatory market scoping, eMarketplace parameters, and fit-for-purpose modalities).
3. Assisting with document guidelines for MSU-Gensan procurement tracking logs.
4. Keeping tracking protocols strictly aligned with SUC (State Universities and Colleges) regulations.

Maintain a structured, helpful, and compliance-first academic tone. Always refer to MSU-Gensan protocols when answering.
"""

# 2. Initialize Conversation Memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Magandang araw! I am your Isko BidDo AI Inquiry Assistant. How can I help you navigate MSU-Gensan procurement guidelines or RA 12009 rules today?"}
    ]

# 3. Render Log History
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. Sidebar: Isko BidDo Quick Reference Templates
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Mindanao_State_University_System_Seal.svg", width=100)
st.sidebar.header("📋 Isko BidDo Quick Inquiries")
st.sidebar.markdown("Select a core capstone focus area to review structural parameters:")

template_choice = st.sidebar.selectbox(
    "Select Topic Context:",
    [
        "General Inquiry...",
        "RA 12009 (NGPA) Transition",
        "MSU-Gensan PPMP Workflow",
        "BAC Logbook Requirements"
    ]
)

# Set dynamic input placeholder text based on the capstone variables
input_placeholder = "Ask about MSU procurement or RA 12009..."
if template_choice == "RA 12009 (NGPA) Transition":
    input_placeholder = "What are the major changes from RA 9184 to RA 12009 regarding State Universities?"
elif template_choice == "MSU-Gensan PPMP Workflow":
    input_placeholder = "Explain the connection between the Project Procurement Management Plan (PPMP) and the Annual Procurement Plan (APP)."
elif template_choice == "BAC Logbook Requirements":
    input_placeholder = "What information must be recorded in the digital logbook for BAC accountability tracking?"

# 5. Local Mock Knowledge Engine (Simulating the AI response stream)
def generate_isko_biddo_response(user_query):
    query = user_query.lower()
    
    if "12009" in query or "ngpa" in query or "transition" in query:
        response_text = (
            "### ⚖️ RA 12009 (New Government Procurement Act) Guidelines\n"
            "Under **RA 12009**, MSU-Gensan transitions into modern, principle-based procurement. Key aspects include:\n\n"
            "1. **Fit-for-Purpose Modalities:** Shifts focus away from strict lowest-bid constraints toward value-for-money mechanics.\n"
            "2. **Mandatory Market Scoping:** Requires explicit documentation of local market research before setting the Approved Budget for the Contract (ABC).\n"
            "3. **eMarketplace Integration:** Utilizing the updated PhilGEPS eMarketplace layout for common-use electronics, supplies, and software options."
        )
    elif "ppmp" in query or "app" in query or "workflow" in query:
        response_text = (
            "### 📋 MSU-Gensan PPMP to APP Process\n"
            "According to standard SUC guidelines outlined in your documentation:\n\n"
            "- **PPMP:** Every end-user department within MSU-Gensan must prepare their *Project Procurement Management Plan* detailing items, timeline, and estimated funds.\n"
            "- **Consolidation:** The Procurement Office or BAC merges all departmental PPMPs into the university-wide **Annual Procurement Plan (APP)**.\n"
            "- **Compliance Rule:** No government procurement can proceed at MSU unless it is strictly specified within an approved APP."
        )
    elif "logbook" in query or "bac" in query or "record" in query:
        response_text = (
            "### 📝 Isko BidDo Digital Logbook Logging Standards\n"
            "To support BAC auditing, accountability, and tracking transparency, the digital system logs:\n\n"
            "- **Transaction ID & PR Number:** For primary key auditing.\n"
            "- **End-User College/Department:** (e.g., CNSM, COED, COE).\n"
            "- **Current Mode of Procurement:** (e.g., Public Bidding, Small Value Procurement, Direct Contracting).\n"
            "- **Status Lifecycle timestamps:** Tracking delay choke-points between request submission, BAC evaluation, and final award."
        )
    else:
        response_text = (
            f"Received request regarding: *\"{user_query}\"*\n\n"
            "Isko BidDo system check complete. As an AI inquiry assistant customized for your MSU-Gensan capstone project framework, "
            "I can analyze this issue in compliance with government auditing requirements."
        )

    # Break string into tokens to animate step-by-step typewriter flow natively
    for word in response_text.split(" "):
        yield word + " "
        time.sleep(0.06)

# 6. Chat Input Execution Loop
if prompt := st.chat_input(input_placeholder):
    
    # Render user prompt immediately
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Append input to memory array
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render assistant animated stream
    with st.chat_message("assistant"):
        final_stream_output = st.write_stream(generate_isko_biddo_response(prompt))
        
    # Record output stream to memory array
    st.session_state.messages.append({"role": "assistant", "content": final_stream_output})
