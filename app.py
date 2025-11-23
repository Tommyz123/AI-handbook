"""
Employee Handbook Intelligent Q&A System - Main Application
Built with Streamlit
"""
import streamlit as st
from document_processor import DocumentProcessor, DocumentProcessingError
from qa_engine import QAEngine, LLMAPIError
from config import Config
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Employee Handbook Q&A System",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 Employee Handbook Q&A System")
st.markdown("---")

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "qa_engine" not in st.session_state:
    st.session_state.qa_engine = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "current_mode" not in st.session_state:
    st.session_state.current_mode = Config.MODE

# Sidebar - Mode selection
with st.sidebar:
    st.header("⚙️ Settings")
    
    mode = st.radio(
        "Select Mode",
        ["Free Mode (Simple Retrieval)", "Paid Mode (OpenAI)"],
        help="Free mode returns document content directly; Paid mode uses AI to summarize answers"
    )
    
    # Update configuration
    new_mode = "free" if "Free" in mode else "paid"
    
    if new_mode != st.session_state.current_mode:
        # Mode changed, reinitialize
        Config.MODE = new_mode
        st.session_state.current_mode = new_mode
        if st.session_state.vector_store is not None:
            try:
                st.session_state.qa_engine = QAEngine(st.session_state.vector_store)
                logger.info(f"Switched to {new_mode} mode")
            except Exception as e:
                st.error(f"Mode switch failed: {e}")
    else:
        Config.MODE = new_mode
    
    # Display mode status
    if Config.MODE == "free":
        st.info("💡 Free Mode: Returns document content directly")
    else:
        if Config.OPENAI_API_KEY:
            st.success("✅ API Key loaded from .env")
        else:
            st.error("❌ API Key not found")
            st.info("💡 Please set in .env file:\nMODE=paid\nOPENAI_API_KEY=your_key")
    
    st.markdown("---")
    st.markdown("### 📊 Usage Statistics")
    st.metric("Questions Asked", st.session_state.question_count)
    
    # Clear cache button
    if st.button("🗑️ Clear Cache"):
        st.session_state.vector_store = None
        st.session_state.qa_engine = None
        st.session_state.chat_history = []
        st.session_state.question_count = 0
        st.success("✅ Cache cleared")
        st.rerun()

# Auto-load handbook.pdf vector store (load saved version first)
if st.session_state.vector_store is None:
    with st.spinner("Loading employee handbook..."):
        try:
            processor = DocumentProcessor()
            
            # Try to load saved vector store first
            try:
                st.session_state.vector_store = processor.load_vector_store("handbook")
                st.success("✅ Vector store loaded (fast startup)")
                logger.info("Loaded vector store from cache")
            except:
                # Vector store doesn't exist, process PDF
                if os.path.exists("handbook.pdf"):
                    st.info("First run, processing PDF...")
                    st.session_state.vector_store = processor.process_pdf("handbook.pdf")
                    st.success("✅ PDF processed, vector store saved!")
                    logger.info("PDF processed and vector store saved")
                else:
                    st.error("❌ handbook.pdf not found")
                    st.info("💡 Please place your employee handbook PDF as handbook.pdf in the current directory")
                    st.stop()
            
            # Initialize QA engine
            st.session_state.qa_engine = QAEngine(st.session_state.vector_store)
            logger.info("QA engine initialized")
            
        except ValueError as e:
            st.error(f"❌ Configuration error: {e}")
            st.info("💡 Please set OPENAI_API_KEY in .env file or switch to free mode")
            st.stop()
        except Exception as e:
            st.error(f"❌ Loading failed: {e}")
            st.info("💡 Please ensure handbook.pdf exists")
            logger.exception("Loading error")
            st.stop()

# Main interface - Q&A area
st.header("💬 Ask a Question")

question = st.text_input(
    "Enter your question",
    placeholder="e.g., How many vacation days do I get?",
    key="question_input"
)

if st.button("🔍 Submit Question", type="primary") and question:
    with st.spinner("Finding answer..."):
        try:
            answer, sources = st.session_state.qa_engine.answer_question(question)
            
            # Update statistics
            st.session_state.question_count += 1
            
            # Add to history
            st.session_state.chat_history.append({
                "question": question,
                "answer": answer,
                "sources": sources
            })
            
            logger.info(f"Question answered: {question}")
            
        except LLMAPIError as e:
            st.error(f"❌ Answer generation failed: {e}")
            st.info("💡 Please check .env configuration or switch to free mode")
            logger.error(f"LLM API error: {e}")
            
        except Exception as e:
            st.error(f"❌ Unknown error: {e}")
            logger.exception("Unexpected error during Q&A")

# Display Q&A history
if st.session_state.chat_history:
    st.markdown("---")
    st.header("📝 Q&A History")
    
    for i, item in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"❓ {item['question']}", expanded=(i == 0)):
            st.markdown("### 💡 Answer")
            st.write(item["answer"])
            
            if item["sources"]:
                st.markdown("### 📍 Sources")
                for source in item["sources"]:
                    section_info = f" - {source['section']}" if source.get('section') else ""
                    st.markdown(f"""
                    **Page {source['page']}{section_info}** (Relevance: {source['score']:.2f})
                    > {source['content']}
                    """)
            else:
                st.info("No relevant sources found")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>Employee Handbook Q&A System v1.0 | 
        <a href="https://github.com" target="_blank">GitHub</a> | 
        Technical Support</small>
    </div>
    """,
    unsafe_allow_html=True
)

# Example questions
with st.expander("💡 Example Questions"):
    st.markdown("""
    - How many vacation days do I get?
    - What is the remote work policy?
    - How do I submit expense reports?
    - What health insurance does the company provide?
    - What are the flexible working hours?
    - What is the professional development budget?
    """)
