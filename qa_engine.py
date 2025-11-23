"""
Q&A Engine Module
Handles question retrieval, answer generation, and source tracking
"""
from typing import List, Dict, Tuple
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from config import Config
import logging
import os
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMAPIError(Exception):
    """LLM API call exception"""
    pass


class QAEngine:
    """Q&A Engine - Lazy initialization of LLM"""
    
    def __init__(self, vector_store: FAISS):
        self.config = Config()
        self.vector_store = vector_store
        self.cache = {}
        self._llm = None  # Lazy initialization
    
    def _get_llm(self):
        """Get LLM (lazy initialization, check mode on each call)"""
        if self.config.MODE == "paid":
            if not self.config.OPENAI_API_KEY:
                raise ValueError("Please set OPENAI_API_KEY in .env file")
            
            # Initialize LLM if not already done
            if self._llm is None:
                logger.info(f"Initializing OpenAI LLM: {self.config.LLM_MODEL}")
                self._llm = ChatOpenAI(
                    model=self.config.LLM_MODEL,
                    temperature=self.config.LLM_TEMPERATURE,
                    openai_api_key=self.config.OPENAI_API_KEY
                )
            return self._llm
        return None
    
    def search_relevant_chunks(self, question: str) -> List[Dict]:
        """Search for relevant document chunks"""
        try:
            results = self.vector_store.similarity_search_with_score(
                question,
                k=self.config.TOP_K
            )
            
            chunks = []
            for doc, score in results:
                chunks.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)
                })
            
            logger.info(f"✅ Retrieved {len(chunks)} relevant document chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []
    
    def generate_answer_openai(self, question: str, context: str) -> str:
        """Generate answer using OpenAI (AI summarization)"""
        try:
            llm = self._get_llm()
            if llm is None:
                raise LLMAPIError("Paid mode not properly configured")
            
            prompt = self.config.PROMPT_TEMPLATE.format(
                context=context,
                question=question
            )
            
            response = llm.invoke(prompt)
            answer = response.content
            
            logger.info(f"✅ OpenAI answer generated successfully")
            return answer
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise LLMAPIError(f"OpenAI API error: {e}")
    
    def generate_simple_answer(self, question: str, context: str) -> str:
        """Simple context-based answer generation (free mode)"""
        logger.info("Using free mode to generate answer")
        
        lines = context.split('\n')
        relevant_lines = []
        current_page = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('[Source:'):
                match = re.search(r'Page (\d+)', line)
                if match:
                    current_page = match.group(1)
            elif line and current_page:
                relevant_lines.append(f"• {line}")
        
        if relevant_lines:
            answer = f"According to the employee handbook (Page {current_page}), here is the relevant information:\n\n"
            answer += '\n'.join(relevant_lines[:15])
            return answer
        else:
            return "Sorry, no relevant information found in the handbook."
    
    def answer_question(self, question: str) -> Tuple[str, List[Dict]]:
        """Answer question"""
        # Check cache
        if self.config.ENABLE_CACHE and question in self.cache:
            logger.info(f"✅ Using cached answer")
            return self.cache[question]
        
        # 1. Retrieve relevant documents
        relevant_chunks = self.search_relevant_chunks(question)
        
        if not relevant_chunks:
            logger.warning("No relevant documents found")
            return "Sorry, no relevant information found in the handbook.", []
        
        # 2. Build context
        context = "\n\n".join([
            f"[Source: Page {chunk['metadata'].get('page', '?')}]\n{chunk['content']}"
            for chunk in relevant_chunks
        ])
        
        # 3. Generate answer
        try:
            if self.config.MODE == "paid":
                answer = self.generate_answer_openai(question, context)
            else:
                answer = self.generate_simple_answer(question, context)
        except LLMAPIError as e:
            logger.error(f"Answer generation failed: {e}")
            answer = f"Sorry, an error occurred while generating the answer: {e}"
        
        # 4. Format sources
        sources = self.format_sources(relevant_chunks)
        
        # Cache result
        if self.config.ENABLE_CACHE:
            self.cache[question] = (answer, sources)
        
        return answer, sources
    
    def format_sources(self, chunks: List[Dict]) -> List[Dict]:
        """Format source information"""
        sources = []
        for chunk in chunks:
            content = chunk["content"]
            if len(content) > 200:
                content = content[:200] + "..."
            
            sources.append({
                "page": chunk["metadata"].get("page", "?"),
                "section": chunk["metadata"].get("section", ""),
                "content": content,
                "score": chunk.get("score", 0)
            })
        
        return sources


if __name__ == "__main__":
    try:
        from document_processor import DocumentProcessor
        
        Config.validate()
        processor = DocumentProcessor()
        
        if os.path.exists("handbook.pdf"):
            try:
                vector_store = processor.load_vector_store()
            except:
                vector_store = processor.process_pdf("handbook.pdf")
            
            qa_engine = QAEngine(vector_store)
            
            test_questions = [
                "How many vacation days do I get?",
                "What is the remote work policy?"
            ]
            
            for question in test_questions:
                print(f"\nQuestion: {question}")
                answer, sources = qa_engine.answer_question(question)
                print(f"Answer: {answer}")
        else:
            print("⚠️ handbook.pdf not found")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
