# =============================================================================
# Streamlit Application for RAG Assistant
# =============================================================================
# This is the user interface. It imports our backend modules and handles:
# - Page layout and configuration
# - User input (chat, sidebar settings)
# - Displaying responses and sources
# - Session state management
# =============================================================================

import streamlit as st
import os
from backend.database import RAGDatabase
from backend.agent import RAGAgent
import config

# -----------------------------------------------------------------------------
# Page Configuration (must be first Streamlit command)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TOPIC RAG Assistant",
    page_icon="📖",
    layout="wide"
)
# -----------------------------------------------------------------------------
# Friends Theme Styling (Purple background + Yellow accents)
# -----------------------------------------------------------------------------
FRIENDS_PURPLE = "#7B5CD6"
FRIENDS_YELLOW = "#F3D45C"
FRIENDS_BLACK  = "#111111"
FRIENDS_WHITE  = "#FFFFFF"

st.markdown("""
<style>
/* Purple app background */
.stApp {
    background-color: #7B5CD6;
}

/* Sidebar style */
section[data-testid="stSidebar"] {
    background-color: rgba(0,0,0,0.35);
    border-right: 4px solid #F3D45C;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

/* Headers */
h1, h2, h3 {
    color: #FFFFFF;
}

/* Alert boxes (success / warning / error / info) */
div[data-testid="stAlert"] {
    font-weight: 700;
    background-color: #F3D45C !important;
    border: 3px solid #000000 !important;
    border-radius: 14px;
    color: #000000 !important;
}

/* Force all text inside alerts to be black */
div[data-testid="stAlert"] * {
    color: #000000 !important;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    background-color: #F3D45C !important;
    border: 3px solid #000000 !important;
    border-radius: 18px;
    color: #000000 !important;
    padding: 0.75rem;
    margin-bottom: 0.75rem;
}

div[data-testid="stChatMessage"] p {
    color: #000000 !important;
}

/* Expanders */
details {
    background-color: #F3D45C !important;
    border: 3px solid #000000 !important;
    border-radius: 16px !important;
}

summary {
    color: #000000 !important;
    font-weight: 800 !important;
}

/* Chat input */
div[data-testid="stChatInput"] {
    border: 3px solid #F3D45C;
    border-radius: 16px;
    background-color: rgba(0,0,0,0.25);
}

/* Buttons */
.stButton > button {
    background-color: #F3D45C;
    border: 3px solid #000000;
    color: #000000;
    font-weight: 800;
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)
# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
# IMPORTANT: Streamlit reruns this entire file every time the user:
# - Types a message
# - Clicks a button  
# - Moves a slider
#
# Without session state, our chat history would vanish on every interaction.
# st.session_state store a dictionary on session information that should persist
# through user interactions.
# 
# Pattern: if 'key' not in st.session_state: st.session_state.key = default
# -----------------------------------------------------------------------------

# Chat history - list of {"role": "user"/"assistant", "content": "..."}
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Database path from sidebar
if 'db_path' not in st.session_state:
    st.session_state.db_path = config.DEFAULT_DB_PATH

# Number of results to retrieve
if 'top_k' not in st.session_state:
    st.session_state.top_k = config.DEFAULT_TOP_K

# Database instance (expensive to create, so we cache it)
if 'database' not in st.session_state:
    st.session_state.database = None


# -----------------------------------------------------------------------------
# Sidebar - User Configuration
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # TO DO: API Key input
    # Make sure the user can hide their input
    api_key = st.text_input("OpenAI API Key",
                            type = "password",
                            help = "Enter your OpenAI API Key")
    
    # TO DO: Database path input via config.py
    db_path = st.text_input("Database Path",
                            value = config.DEFAULT_DB_PATH,
                            help = "Path to you DuckDB vector database")
    
    # Store in session state
    st.session_state.db_path = db_path
    
    # TO DO: Top K results with an interactive slider bar
    top_k = st.slider("Results per Query",
                      min_value=3,
                      max_value=20,
                      value = config.DEFAULT_TOP_K,
                      help = "Number of passages to retrieve per search")

    # Store in session state
    st.session_state.top_k = top_k
    
    # TO DO: Model selection dropdown menu
    model_choice = st.selectbox("LLM Model",
                                config.AVAILABLE_MODELS,
                                index = 0)
    
    # TO DO: Create max_iter slider
    # Max iterations for tool calls
    max_iter = st.slider("Max Tools Calls",
                         min_value = 1,
                         max_value = 5,
                         value = config.DEFAULT_MAX_ITER,
                         help = "Maximum Number of database queries per question")
    
    st.divider()
    
    # TO DO: Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    
    # TO DO: Update for your project
    st.markdown("""
    ### About

This RAG assistant explores *Friends* as a reflection of real life rather than just a TV show.

It is designed to help users understand how the series portrays:
- friendship as chosen family
- relationships, dating, and emotional vulnerability
- humor as a way of coping with everyday struggles
- the shared experiences of early adulthood

The assistant generates responses by retrieving and synthesizing insights from a curated collection of analyses, essays, and commentaries about *Friends*, using semantic search and embeddings to ground each answer in the source material.
    """)

# -----------------------------------------------------------------------------
# Main App Header
# -----------------------------------------------------------------------------
st.markdown("<style>...</style>", unsafe_allow_html=True)

# MAIN HEADER SECTION
st.title("🚪👫 The One Where Friends Feels Real")
st.image("LASTNAME_LPP_Rag/ASSETS/door.png", width=160)
# -----------------------------------------------------------------------------
# Central Perk Welcome Section
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div style="
        background-color:#F3D45C;
        border:3px solid #000000;
        border-radius:18px;
        padding:1.2rem;
        margin-top:1.5rem;
        margin-bottom:1.5rem;
        text-align:center;
        color:#000000;
        font-weight:600;
    ">
        ☕ <strong>Welcome to Central Perk</strong> <br><br>
        This guide is here to help you explore how <i>Friends</i> reflects real life, 
        from friendship and relationships to humor and growing up.
        <br><br>
        Try asking about the characters, their relationships, or why the show still resonates today.
    </div>
    """,
    unsafe_allow_html=True
)
# -----------------------------------------------------------------------------
# Database Connection
# -----------------------------------------------------------------------------
# Recreate database instance if path changed from default in case multiple duckdb files
if not st.session_state.database or st.session_state.database.db_path != db_path:
    st.session_state.database = RAGDatabase(db_path)

# Test and display connection status
if not st.session_state.database.test_connection():
    st.error(f"❌ Database not found at: `{db_path}`")
    st.info("Please update the database path in the sidebar.")
    if not os.path.exists(db_path):
        st.stop() # Stop execution here - can't continue without database
else:
    st.success(f"✅ Database connected: `{db_path}`")

# -----------------------------------------------------------------------------
# API Key Check
# -----------------------------------------------------------------------------
if not api_key:
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to continue.")
    st.stop()

# Set the API key as environment variable (OpenAI client reads from here)
os.environ["OPENAI_API_KEY"] = api_key

# -----------------------------------------------------------------------------
# Display Chat History
# -----------------------------------------------------------------------------
# Loop through all previous messages and display them
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources for assistant messages if available
        if message["role"] == "assistant" and message.get("sources"):

            # Creates expander bar and allows user to view sources
            with st.expander(f"View Sources ({len(message['sources'])} passages retrieved)"):
                
                # Loops over source number and content
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"**Source {i}** (Similarity: {source['similarity']:.3f})")
                    st.text_area(
                        f"Chunk {i}",
                        source["text"],
                        height=150,
                        key=f"source_{id(message)}_{i}",
                        label_visibility="collapsed"
                    )
                    st.divider()

# -----------------------------------------------------------------------------
# Chat Input and Response Generation
# -----------------------------------------------------------------------------
# st.chat_input returns None until user submits, then returns their text
# The := (walrus operator) assigns AND checks in one line

if prompt := st.chat_input("Ask a question about Friends..."):
    
    # TO DO: Add user message to history
    st.session_state.messages.append({"role":"user", "content":prompt})

    # TO DO: Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching database and generating answer..."):
            try:
                # TO DO: Initialize Agent
                agent = RAGAgent(db = st.session_state.database,
                                 model_name = model_choice,
                                 max_iter = max_iter)
                
                # Get answer
                result = agent.ask(prompt)
                response = result["answer"]
                sources = result["sources"]
                
                st.markdown(response)
                
                # Display sources immediately
                if sources:
                    with st.expander(f"📚 View Sources ({len(sources)} passages retrieved)"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(f"**Source {i}** (Similarity: {source['similarity']:.3f})")
                            st.text_area(
                                f"Passage {i}",
                                source["text"],
                                height=150,
                                key=f"source_new_{i}",
                                label_visibility="collapsed"
                            )
                            if i < len(sources):
                                st.divider()
                
                # Add to history with sources
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "sources": sources
                })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "sources": []
                })

# TO DO: Example questions in an expander
with st.expander("💡 Example Questions"):
    examples = [
        "How does Friends reflect the challenges of early adulthood?",
        "Why does the friend group feel like a chosen family?",
        "How does humor (like sarcasm) help characters deal with stress?",
        "Why do people find Friends so comforting to rewatch?",
        "What relationship patterns show up repeatedly across the characters?"
    ]
    
    for example in examples:
        if st.button(example, key=example):
            # Simulate entering the question
            st.session_state.messages.append({"role": "user", "content": example})
            st.rerun()
