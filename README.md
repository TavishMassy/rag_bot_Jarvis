# 🏛️ VGU One Policy Assistant (Enterprise RAG)

An intelligent, authoritative student success AI designed to provide 100% accurate information from the **VGU Student Handbook 2025**. This project demonstrates a production-ready **Retrieval-Augmented Generation (RAG)** pipeline.

---

## 🛠️ Infrastructure & Tech Stack

### 🚀 Backend: Hugging Face Docker Space (n8n)
The "Brain" of this project is a self-hosted **n8n orchestration engine** running within a custom **Docker container** on Hugging Face Spaces.
- **Environment:** Linux / Node.js 20 Alpine
- **Persistence:** Custom volume mapping for encrypted credential storage.
- **Security:** Bypasses ephemeral storage restrictions using root-level permission overrides (`chmod 777`) to ensure reliable performance.



### 🧠 Intelligence: Google Gemini 1.5 Flash
- **Model:** `gemini-1.5-flash`
- **Role:** Synthesis of retrieved handbook text into natural, professional language.
- **Constraint:** Strictly limited to provided context to ensure **zero hallucinations**.

### 📁 Database: Supabase (pgvector)
- **Storage:** Vectorized embeddings of the VGU Student Handbook 2025.
- **Retrieval:** Similarity search using `text-embedding-004` to match user queries with handbook clauses.

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
3. Import `VGU_Workflow.json`.

### Frontend (Streamlit)
1. Clone this repo.
2. Update `N8N_WEBHOOK_URL` in `app.py` with your HF Space link.
3. Run `streamlit run app.py`.

---
