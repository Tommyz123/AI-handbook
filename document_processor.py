"""
文档处理模块
负责 PDF 解析、文本分割、向量化和向量库构建
向量化始终使用免费的本地模型
"""
import os
# 修复 sentence-transformers 的 PyTorch meta tensor 问题
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

import pdfplumber
import re
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import Config
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentProcessingError(Exception):
    """文档处理异常"""
    pass


class DocumentProcessor:
    """文档处理器 - 向量化始终使用免费模型"""
    
    def __init__(self):
        self.config = Config()
        
        # 向量化始终使用免费的本地模型（不随模式切换）
        logger.info(f"使用免费 Embedding 模型: {self.config.EMBEDDING_MODEL}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.EMBEDDING_MODEL
        )
        
        # 备用的通用文本分割器
        self.fallback_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " "],
            keep_separator=True
        )
    
    def load_pdf(self, pdf_path: str) -> List[Dict]:
        """加载 PDF 文件并提取文本"""
        try:
            documents = []
            
            with pdfplumber.open(pdf_path) as pdf:
                logger.info(f"正在处理 PDF: {pdf_path}, 总页数: {len(pdf.pages)}")
                
                for page_num, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text()
                    if text:
                        # 清理文本
                        text = text.replace("(cid:127)", "-")
                        
                        documents.append({
                            "content": text,
                            "metadata": {
                                "page": page_num,
                                "source": os.path.basename(pdf_path)
                            }
                        })
            
            logger.info(f"✅ PDF 加载完成，共 {len(documents)} 页")
            return documents
            
        except Exception as e:
            logger.error(f"PDF 加载失败: {e}")
            raise DocumentProcessingError(f"无法读取 PDF 文件: {e}")
    
    def split_by_sections(self, text: str) -> List[Dict]:
        """按章节切割员工手册"""
        chunks = []
        sections = re.split(r'(\d+\.\s+[A-Z][^\n]+)', text)
        
        current_section = None
        current_content = []
        
        for part in sections:
            if re.match(r'\d+\.\s+[A-Z]', part):
                if current_section:
                    content_text = '\n'.join(current_content)
                    chunks.append({
                        'section': current_section,
                        'content': content_text,
                        'char_count': len(content_text)
                    })
                
                current_section = part.strip()
                current_content = [part]
            elif part.strip():
                current_content.append(part)
        
        if current_section:
            content_text = '\n'.join(current_content)
            chunks.append({
                'section': current_section,
                'content': content_text,
                'char_count': len(content_text)
            })
        
        logger.info(f"✅ 按章节切割完成，共 {len(chunks)} 个章节")
        return chunks
    
    def split_documents(self, documents: List[Dict], use_section_split: bool = True) -> List[Dict]:
        """分割文档为小块"""
        try:
            full_text = '\n'.join([doc["content"] for doc in documents])
            
            if use_section_split:
                section_chunks = self.split_by_sections(full_text)
                
                if len(section_chunks) > 0:
                    logger.info(f"使用章节切割策略")
                    chunks = []
                    for i, chunk in enumerate(section_chunks):
                        estimated_page = min(i + 1, len(documents))
                        chunks.append({
                            "content": chunk["content"],
                            "metadata": {
                                "section": chunk["section"],
                                "page": estimated_page,
                                "chunk_id": i,
                                "source": documents[0]["metadata"]["source"]
                            }
                        })
                    return chunks
            
            # 回退到通用切割
            logger.info(f"使用通用切割策略")
            chunks = []
            for doc in documents:
                text_chunks = self.fallback_splitter.split_text(doc["content"])
                
                for i, chunk in enumerate(text_chunks):
                    chunks.append({
                        "content": chunk,
                        "metadata": {
                            **doc["metadata"],
                            "chunk_id": i
                        }
                    })
            
            logger.info(f"✅ 文档分割完成，共 {len(chunks)} 个块")
            return chunks
            
        except Exception as e:
            logger.error(f"文档分割失败: {e}")
            raise DocumentProcessingError(f"文本处理错误: {e}")
    
    def build_vector_store(self, chunks: List[Dict]) -> FAISS:
        """构建向量数据库"""
        try:
            texts = [chunk["content"] for chunk in chunks]
            metadatas = [chunk["metadata"] for chunk in chunks]
            
            logger.info(f"正在生成向量... (共 {len(texts)} 个文档块)")
            
            vector_store = FAISS.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas
            )
            
            logger.info(f"✅ 向量库构建完成")
            return vector_store
            
        except Exception as e:
            logger.error(f"向量化失败: {e}")
            raise DocumentProcessingError(f"向量生成失败: {e}")
    
    def save_vector_store(self, vector_store: FAISS, name: str = "handbook"):
        """保存向量数据库到本地"""
        try:
            save_path = os.path.join(self.config.VECTOR_STORE_DIR, name)
            vector_store.save_local(save_path)
            logger.info(f"✅ 向量库已保存到: {save_path}")
        except Exception as e:
            logger.error(f"向量库保存失败: {e}")
            raise DocumentProcessingError(f"无法保存向量库: {e}")
    
    def load_vector_store(self, name: str = "handbook") -> FAISS:
        """从本地加载向量数据库"""
        try:
            load_path = os.path.join(self.config.VECTOR_STORE_DIR, name)
            vector_store = FAISS.load_local(
                load_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info(f"✅ 向量库已加载: {load_path}")
            return vector_store
        except Exception as e:
            logger.error(f"向量库加载失败: {e}")
            raise DocumentProcessingError(f"无法加载向量库: {e}")
    
    def process_pdf(self, pdf_path: str) -> FAISS:
        """完整的 PDF 处理流程"""
        logger.info(f"开始处理 PDF: {pdf_path}")
        
        # 1. 加载 PDF
        documents = self.load_pdf(pdf_path)
        
        # 2. 分割文档
        chunks = self.split_documents(documents)
        
        # 3. 构建向量库
        vector_store = self.build_vector_store(chunks)
        
        # 4. 保存向量库
        self.save_vector_store(vector_store)
        
        logger.info(f"✅ PDF 处理完成！")
        return vector_store


if __name__ == "__main__":
    try:
        Config.validate()
        processor = DocumentProcessor()
        
        if os.path.exists("handbook.pdf"):
            vector_store = processor.process_pdf("handbook.pdf")
            print(f"\n✅ 测试成功！向量库已创建")
        else:
            print("⚠️ 未找到 handbook.pdf")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
