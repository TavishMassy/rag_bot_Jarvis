import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="VGU One | Ai Assistant", layout="centered")

# 2. Refined CSS (Forced Background and Tab Styling)
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(to bottom, #fea, #ffbab3);
            background-size: cover;
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

        /* Targets the actual text area inside the chat input */
        [data-testid="stChatInput"] textarea {
            background-color: white !important;
            -webkit-text-fill-color: black !important;
        }

        [data-testid="stChatInput"] > div {
            background-color: #f9f9f9 !important;
        }

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
            color: black !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
        }

        /* Tab Styling */
        button[data-baseweb="tab"]:hover p {
            color: #ff4448 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# 3. Create the Top Navigation Tabs (No Emojis, clean corporate text)
tab_chat, tab_about, tab_connect = st.tabs(["AI Chat", "Architecture", "Connect"])

with tab_chat:
    st.markdown("""
    <div class="vgu-header">
        <div>
            <p class="vgu-title">VGU One AI Assistant</p>
            <p class="vgu-subtitle">VGU Handbook, Hostel, Clubs and ACIC Knowledge Base</p>
            <div class="vgu-accent-bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    N8N_WEBHOOK_URL = "https://Tamtedd-n8n.hf.space/webhook/5f8469c2-9254-49bd-8936-b9647b3b36ef"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "**Hello! How can I help you?**\n\nYou can ask me any question, such as:\n* *How can I join CST club?*\n* *How does the grading system work?*\n* *How can I apply for a hostel room?*\n\n"}]

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
    <div class="info-panel" style="color: #393939; line-height: 1.6;">
        <h2 style="margin-top:0; color: rgb(129, 24, 17); border-bottom: 2px solid #F18F2C; padding-bottom: 10px;">System Architecture</h2>
        <p>A production-ready <strong>Retrieval-Augmented Generation (RAG)</strong> pipeline designed for super accurate university knowledge base automation.</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid rgb(129, 24, 17);">
                <h4 style="margin-top:0;">🚀 Backend: n8n + Docker</h4>
                <p style="font-size: 0.9rem;">Hosted on <strong>Hugging Face Spaces</strong> using a custom <strong>Node-Alpine</strong> Docker container. Optimized for low-latency orchestration and secure volume mapping for data persistence.</p>
            </div>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #F18F2C;">
                <h4 style="margin-top:0;">🧠 Intelligence: Gemini AI</h4>
                <p style="font-size: 0.9rem;">Leveraging <strong>Google Gemini 2.5 Flash Lite</strong> for synthesis. The model is strictly grounded to retrieved context, eliminating hallucinations and ensuring institutional accuracy.</p>
            </div>
        </div>
        <h3 style="color: rgb(129, 24, 17); margin-top: 25px;">The Data Pipeline</h3>
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 10px;">🔹 <strong>Vector Storage:</strong> Official handbooks (PDFs) are vectorized and stored in <strong>Supabase (pgvector)</strong> for high-speed semantic retrieval.</li>
            <li style="margin-bottom: 10px;">🔹 <strong>Hardened Security:</strong> Protected against prompt injection via strict system directives and UUID-based webhook obscurity.</li>
            <li style="margin-bottom: 10px;">🔹 <strong>Persistence:</strong> Custom volume mapping ensures API credentials and session states remain intact across cloud reboots.</li>
        </ul>
        <p style="font-size: 0.8rem; color: #555; margin-top: 2rem; border-top: 1px solid #e5e5e5; padding-top: 10px;">
            <strong>Caution:</strong> This is an AI-powered assistant. While grounded in official documentation, always verify critical information against the official VGU handbooks.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 3: CONNECT ---
with tab_connect:
    st.markdown("""
    <div class="info-panel" style="color: #393939; line-height: 1.6;">
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <div style="background: rgb(129, 24, 17); color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold;">
                TM
            </div>
            <div>
                <h2 style="margin: 0; color: rgb(129, 24, 17);">Tavish Massy</h2>
                <p style="margin: 0; font-weight: 600; color: #525252;">AI Automation Developer</p>
            </div>
        </div>
        <p>I am a First-Year AI/ML student at <strong>Vivekananda Global University</strong>, specializing in the deployment of autonomous agents and production-grade RAG pipelines. My work focuses on bridging the gap between raw data and actionable AI intelligence.</p>   
        <h3 style="color: rgb(129, 24, 17); border-bottom: 1px solid #e5e5e5; padding-bottom: 5px;">Technical Knowledge Aquired during this Project</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
            <span style="background: #eee; padding: 4px 12px; border-radius: 15px; font-size: 0.8rem;">Workflow Automation (n8n)</span>
            <span style="background: #eee; padding: 4px 12px; border-radius: 15px; font-size: 0.8rem;">Vector Databases (Supabase/pgvector)</span>
            <span style="background: #eee; padding: 4px 12px; border-radius: 15px; font-size: 0.8rem;">Large Language Models (Gemini/GPT)</span>
            <span style="background: #eee; padding: 4px 12px; border-radius: 15px; font-size: 0.8rem;">Docker & Cloud Hosting</span>
            <span style="background: #eee; padding: 4px 12px; border-radius: 15px; font-size: 0.8rem;">Python / Streamlit</span>
        </div>
        <div style="margin-top: 30px; display: flex; gap: 15px;">
            <a href="https://www.linkedin.com/in/tavish-massy-b0396a370/" target="_blank" style="text-decoration: none; background-color: rgb(129, 24, 17); color: white; padding: 12px 25px; border-radius: 5px; font-weight: 600; font-size: 0.9rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                Connect on LinkedIn
            </a>
            <a href="https://github.com/TavishMassy" target="_blank" style="text-decoration: none; border: 1px solid rgb(129, 24, 17); color: rgb(129, 24, 17); padding: 12px 25px; border-radius: 5px; font-weight: 600; font-size: 0.9rem;">
                View GitHub
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
