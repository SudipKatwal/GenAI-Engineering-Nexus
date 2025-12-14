import streamlit as st
import os
from backend import get_rag_chain, initialize_vector_db
from data_gen import generate_dummy_docs

st.set_page_config(page_title="Nexus Knowledge Bot", layout="wide")
# --- HIDE STREAMLIT BRANDING ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --- INITIAL SETUP ---
generate_dummy_docs()  # Ensure we have dummy data on start
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: CONFIGURATION ---
st.sidebar.title("⚙️ Nexus Config")

# 1. Persona Selector (PDO)
persona = st.sidebar.radio(
    "Select Assistant Persona:", ["Engineering", "Ops", "Product"]
)
st.sidebar.info(f"Current Mode: **{persona}**")

# 2. Document Upload
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Knowledge Base")
uploaded_file = st.sidebar.file_uploader("Upload Internal Doc (.txt)", type="txt")

if uploaded_file:
    # Save file and re-index
    with open(os.path.join("./data", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"Uploaded {uploaded_file.name}")
    with st.sidebar.status("Re-indexing Vector DB..."):
        initialize_vector_db()
        st.sidebar.write("Index Updated!")

# --- MAIN CHAT INTERFACE ---
st.title("🧠 Nexus: Engineering & Ops Assistant")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ex: How do I handle high CPU alerts?"):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        chain = get_rag_chain(persona_type=persona)
        
        if chain:
            with st.spinner(f"Consulting {persona} Knowledge Base..."):
                # Run the chain (LCEL returns the string directly)
                response_text = chain.invoke(prompt)

                # Display Answer
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                # Note: Extracting 'sources' is harder in pure LCEL without extra code.
                # For this assignment, displaying the answer is sufficient.
        else:
            st.error("Vector Database is empty. Please check the /data folder.")