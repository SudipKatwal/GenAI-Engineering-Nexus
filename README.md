# GenAI Engineering Nexus 🧠🚀

**A Persona-Driven RAG Knowledge Assistant for Engineering Teams.**

This Capstone project demonstrates a production-ready **Retrieval-Augmented Generation (RAG)** application designed to solve knowledge fragmentation in technical teams. It leverages the latest **LangChain (v0.3)** stack, **Google Gemini 1.5**, and **In-Memory Vector Databases** for instant, zero-setup deployment.

---

## 🎯 Project Objectives

### 1. Problem Identification: The "Knowledge Silo"
**The Real-World Problem:** Modern engineering teams suffer from scattered documentation. Critical information—API specs, refund policies, server mitigation steps—is buried in PDFs, text files, and wikis.
* **Engineers** waste time searching for error codes.
* **Product Managers** struggle to find feature constraints.
* **SREs** need instant access to disaster recovery protocols during outages.

**The Solution Gap:** Traditional keyword search fails to understand *intent* or context (e.g., "How do I fix the server?" vs. "What is the server architecture?").

### 2. Solution Design: Context-Aware RAG
We designed a solution that does not just "search" but "understands" the user's role:
* **Persona-Driven Architecture:** The AI adapts its answer style based on who is asking (e.g., Technical & terse for Ops vs. Strategic & descriptive for Product).
* **RAG (Retrieval-Augmented Generation):** Grounding the LLM's answers in *private* internal data (simulated via text files) to prevent hallucinations.
* **Zero-Friction UX:** A streamlined Streamlit interface that requires no database setup.

### 3. System Implementation
The system was built with technical robustness and portability in mind:
* **Frontend:** `Streamlit` for a clean, chat-based UI.
* **Orchestration:** `LangChain` (LCEL) for managing the retrieval pipeline.
* **Vector Store:** `ChromaDB` (In-Memory mode) for fast, lock-free embedding storage.
* **Embeddings:** `HuggingFace (all-MiniLM-L6-v2)` running locally (free & private).
* **LLM:** `Google Gemini 1.5 Flash` for high-speed, low-cost inference.

### 4. Tech-Driven Insight
This project provided hands-on experience with the modern GenAI stack:
* **Migrating from Legacy Chains to LCEL:** Implemented the modern "LangChain Expression Language" pipe syntax (`|`) for better readability and debugging.
* **Hybrid Compute Strategy:** Offloading heavy reasoning to the Cloud (Gemini) while keeping sensitive embeddings local (HuggingFace) for privacy and cost optimization.
* **Singleton Pattern:** Implemented caching strategies in Python to prevent unnecessary database rebuilds.

---

## 🛠️ Technical Stack

| Component | Tool Used | Why? |
| :--- | :--- | :--- |
| **LLM** | Google Gemini 1.5 Flash | High speed, large context window, cost-effective. |
| **Orchestration** | LangChain (v0.3) | Standard industry framework for chaining LLM logic. |
| **Embeddings** | HuggingFace (`all-MiniLM`) | Runs locally on CPU, no API limits, high privacy. |
| **Vector DB** | ChromaDB (In-Memory) | Zero setup, no file-lock errors, instant testing. |
| **UI** | Streamlit | Rapid prototyping for data apps. |

---

## 🚀 How to Run Locally

This project is designed to "just work." No database installation required.

### 1. Clone & Setup
```bash
git clone <repository-url>
cd GenAI-Engineering-Nexus
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate