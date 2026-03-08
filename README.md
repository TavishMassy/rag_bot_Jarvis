# 🏛️ VGU One Ai Assistant (RAG)
https://ragbotjarvis-twhygdejckztzwcyyyrypu.streamlit.app/

An intelligent, authoritative student success AI designed to provide accurate information from the **VGU Student Handbook**, **Hostel Booklet**, **Club Brochure** and **ACIC Document**. This project demonstrates a production-ready **Retrieval-Augmented Generation (RAG)** pipeline.

---

## 🛠️ Infrastructure & Tech Stack


### 🚀 Backend: Hugging Face Docker Space (n8n)
The "Brain" of this project is a self-hosted **n8n orchestration engine** running within a custom **Docker container** on Hugging Face Spaces.


### 🐧 Backend Environment (n8n + Docker)
The orchestration layer is hosted in a **Hugging Face Docker Space** using a customized `node:20-alpine` image.
* **Alpine Linux Base:** I selected a minimal Alpine-based image to reduce the container footprint, resulting in faster deployment cycles and lower memory overhead.
* **Node.js 20:** Ensures compatibility with the latest n8n enterprise features and AI nodes.


### 💾 Data Persistence & Volume Mapping
Hugging Face Spaces utilize **ephemeral storage**, meaning any data saved locally is lost upon container restart. To solve this:
* **Custom Volume Mapping:** I implemented a persistent storage strategy by mapping the n8n user folder (`/root/.n8n`) to a dedicated volume. 
* **Persistence:** This ensures that n8n credentials (Gemini/Supabase API keys) and workflow definitions remain intact even if the cloud instance reboots.


### 🛡️ Security & Access Control
Deploying an AI to the public web requires specific security hardening:
* **Permission Overrides:** To bypass the strict "Read-Only" filesystem of the HF environment, I applied specific `chmod 777` permission overrides during the build process to allow n8n to initialize its internal SQLite database successfully.
* **RAG-Based Hardening:** The system is protected against "Prompt Injection" by a strict system prompt that forces the LLM to derive answers **EXCLUSIVELY** from the Student Handbook.
* **Endpoint Obscurity:** The n8n backend is protected via a unique UUID-based webhook endpoint, preventing unauthorized API calls from external sources.


### 🧠 Intelligence: Google Gemini 2.5 Flash Lite
- **Model:** `gemini-2.5-flash-lite`
- **Role:** Synthesis of retrieved handbook text into natural, professional language.
- **Constraint:** Strictly limited to provided context to ensure **zero hallucinations**.


### 📁 Database: Supabase (pgvector)
- **Storage:** Vectorized embeddings of the documents in `SUPABASE`.
- **Retrieval:** Similarity search using `text-embedding-001` to match user queries with handbook clauses.


### 🎨 Frontend: Streamlit
- **UI:** Custom-styled to match the official **VGU One Portal**.
- **UX:** Top-navigation tabs for seamless switching between Chat, Architecture, and Contact.


---

## 🏗️ System Flow

1.  **Request:** User asks a query on the Streamlit frontend.
2.  **Trigger:** Streamlit sends a POST request to the **n8n Production Webhook** on Hugging Face.
3.  **Search:** n8n queries **Supabase** via vector similarity search.
4.  **Prompting:** n8n sends the retrieved "Context" + User "Query" to **Gemini Flash**.
5.  **Output:** The LLM returns the answer with a **PDF Page Citation**, which is then rendered on the UI.


---

## 📖 Installation & Usage

### Backend (n8n on Hugging Face)
1. Use the provided `Dockerfile` "docker-hugging-space.txt" to spin up an n8n instance on HF Spaces.
2. Set Environment Variables: `N8N_PORT=7860`, `DB_TYPE=sqlite`, `N8N_USER_FOLDER=/root/.n8n`.
   - 🛠️ One quick warning on URLs
    Hugging Face can be picky about trailing slashes.
    When you fill in your variables, make sure they look like this:
    WEBHOOK_URL: https://<user_name>-<space_name>.hf.space (No / at the end)
    N8N_HOST: <user_name>-<space_name>.hf.space (No https:// and no /)
4. Import `VGU_Workflow.json`.

### Frontend (Streamlit)
1. Clone this repo.
2. Update `N8N_WEBHOOK_URL` in `app.py` with your HF Space link.
3. Run `streamlit run app.py`.

---
