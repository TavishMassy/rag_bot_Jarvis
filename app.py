import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="VGU One | Policy Assistant", layout="centered")

# 2. Refined CSS (Forced Background and Tab Styling)
st.markdown("""
    <style>
        /* Targeting the main container for the background */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        }

        /* VGU Primary Header */
        .vgu-header {
            background-color: rgb(129, 24, 17); 
            color: #ffffff;
            padding: 1.5rem;
            border-radius: 8px; 
            text-align: left; 
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .vgu-title { margin: 0; font-weight: 600; font-size: 1.5rem; color: #ffffff !important; }
        .vgu-subtitle { margin: 0; font-weight: 400; font-size: 0.875rem; color: #e5e5e5 !important; }
        .vgu-accent-bar { height: 4px; background-color: #F18F2C; width: 100%; border-radius: 2px; margin-top: 8px; }

        /* Clean Chat Messages */
        .stChatMessage {
            background-color: #ffffff !important; 
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            border: 1px solid #dee2e6; 
        }
        
        /* Ensure text is dark and readable */
        .stChatMessage p, .stChatMessage li {
            color: #212529 !important;
        }

        /* Tab Styling */
        button[data-baseweb="tab"] p {
            color: #212529 !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# 3. Create the Top Navigation Tabs (No Emojis, clean corporate text)
tab_chat, tab_about, tab_connect = st.tabs(["Chat Assistant", "Architecture", "Connect"])

with tab_chat:
    st.markdown("""
    <div class="vgu-header">
        <div>
            <p class="vgu-title">VGU Assistant</p>
            <div class="vgu-accent-bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    N8N_WEBHOOK_URL = "https://Tamtedd-n8n.hf.space/webhook/3150ee5e-b2f3-4d44-9ea8-fd547fa6355c"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "**Hello! Welcome to the VGU One Policy Assistant.**\n\nI am connected directly to the RAG architecture. You can ask me questions about the student handbook, such as:\n* *What different types of clubs are available?*\n* *How does the grading system work?*\n* *What are mess timings?*\n\nHow can I help you today?"}]

    # --- THE FIX: USE A CONTAINER FOR MESSAGES ---
    # This keeps the history separate from the input logic
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input (Placed outside the container so it stays at the absolute bottom)
    if prompt := st.chat_input("Ask here..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Rerender to show the user message immediately
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # Get AI Response
        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Searching..."):
                    try:
                        response = requests.post(N8N_WEBHOOK_URL, json={"chatInput": prompt}, timeout=30)
                        bot_reply = response.json().get("output", "Done.") if response.status_code == 200 else "Error."
                        st.markdown(bot_reply)
                        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    except:
                        st.error("Connection failed.")
        
        # This force-refreshes the page to keep the chat input at the bottom
        st.rerun()

# --- TAB 2: ARCHITECTURE & ABOUT ---
with tab_about:
    st.markdown("""
    <div class="info-panel" style="color: #393939;">
        <h3 style="margin-top:0; color: rgb(129, 24, 17);">System Architecture</h3>
        <p>This application demonstrates an <strong>Retrieval-Augmented Generation (RAG)</strong> pipeline designed to automate HR and administrative policy queries. It acts as a centralized knowledge engine.</p>
        <h4>Data Pipeline</h4>
        <ol>
            <li><strong>Input:</strong> User submits a natural language query via this interface.</li>
            <li><strong>Orchestration:</strong> The payload is intercepted by a custom <strong>n8n</strong> webhook.</li>
            <li><strong>Vector Search:</strong> The query is embedded and cross-referenced against official documents stored inside a <strong>Supabase</strong> pgvector database.</li>
            <li><strong>Synthesis:</strong> <strong>Google Gemini Flash</strong> synthesizes the exact policy, formatting the response with a direct source citation.</li>
        </ol>
        <p style="font-size: 0.8rem; color: #6b7280; margin-top: 2rem; border-top: 1px solid #e5e5e5; padding-top: 10px;">
            <strong>Caution:</strong> This is an AI-powered assistant. While grounded in official documentation, always verify critical information against the official VGU handbooks.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 3: CONNECT ---
with tab_connect:
    st.markdown("""
    <div class="info-panel" style="color: #393939;">
        <h3 style="margin-top:0; color: rgb(129, 24, 17);">Developer Profile</h3>
        <p><strong>Toothy</strong></p>
        <p>1st-Year CSE Student, VGU, Jaipur</p>
        <p>Focusing on building enterprise bots, AI Automation, and Generative AI pipelines.</p>
        <div style="margin-top: 20px;">
            <a href="https://linkedin.com/in/yourprofile" target="_blank" style="text-decoration: none; background-color: rgb(129, 24, 17); color: white; padding: 10px 20px; border-radius: 5px; font-weight: 600; font-size: 0.9rem;">
                Connect on LinkedIn
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)