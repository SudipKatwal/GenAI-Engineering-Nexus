import os
import shutil
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# We use a unique folder name to avoid old permission locks
DB_PATH = "./chroma_db_persistent"
DATA_PATH = "./data"

def initialize_vector_db():
    """Ingests documents and saves them to disk."""
    print("💾 Initialization: Checking database...")

    # 1. Load Data
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        return None
        
    loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()
    if not docs:
        print("⚠️ No data found in /data folder.")
        return None

    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 3. Define Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 4. Handle Existing DB (Delete only if we need a fresh start)
    if os.path.exists(DB_PATH):
        print("♻️  Removing old database to ensure fresh data...")
        try:
            shutil.rmtree(DB_PATH)
            time.sleep(1) # Wait for OS to release file lock
        except PermissionError:
            print("❌ Error: Could not delete old DB. Please delete 'chroma_db_persistent' folder manually.")
            return None

    # 5. Create & Save DB to Disk
    print("📦 Creating new persistent Vector DB...")
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=DB_PATH)
    print("✅ Database saved to disk successfully.")
    return vectorstore

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(persona_type="Engineering"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Check if DB exists on disk
    if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
        # Load existing DB
        vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    else:
        # Create new one if missing
        vectorstore = initialize_vector_db()
        
    if not vectorstore:
        return None

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # FIX: Correct model name
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # --- PROMPT ---
    if persona_type == "Ops":
        role_desc = "You are a Senior Site Reliability Engineer (SRE). Focus on stability, mitigation steps, and command-line solutions."
    elif persona_type == "Product":
        role_desc = "You are a Product Manager. Focus on features, user requirements, and business logic."
    else:
        role_desc = "You are a Senior Backend Engineer. Focus on API specs, implementation details, and architecture."

    system_prompt = (
        f"{role_desc}\n"
        "Task: Answer the query using ONLY the provided context.\n"
        "Constraints:\n"
        "- If the answer is not in the context, say 'Information not found in internal docs'.\n"
        "- Use technical formatting (code blocks) where appropriate.\n"
        "- Be concise and actionable.\n\n"
        "Context:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain
