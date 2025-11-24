# Employee Handbook Q&A System

A simple and user-friendly web tool that allows employees to ask questions about the company handbook in natural language and get accurate answers with source citations.

## ✨ Features

- 📚 **Fixed Handbook**: Uses `handbook.pdf` as the knowledge base
- 💬 **Natural Language Q&A**: Ask questions in plain English or Chinese
- 🌐 **Language Adaptation**: AI responds in the same language as your question
- 📍 **Source Citations**: Shows which page and section the answer comes from
- 🆓 **Dual Mode Support**:
  - Free Mode: Simple document retrieval (no API needed)
  - Paid Mode: AI-powered summarization using OpenAI (better quality)
- 🚀 **One-Click Setup**: Automatic dependency installation and launch
- ⚡ **Fast Startup**: Vector store persistence for quick loading
- 💾 **Smart Caching**: Same questions don't trigger repeated API calls

## 🚀 Quick Start

### Method 1: One-Click Setup (Recommended)

```bash
python setup.py
```

The script will automatically:
- ✅ Install all dependencies
- ✅ Create configuration files
- ✅ Launch the application

### Method 2: Manual Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment variables
cp .env.example .env
# Edit .env file to set MODE and API Key

# 3. Launch application
streamlit run app.py
```

## 📖 Usage Guide

### Step 1: Configure Mode

Edit the `.env` file:

```bash
# For Free Mode (no API key needed)
MODE=free

# For Paid Mode (requires OpenAI API key)
MODE=paid
OPENAI_API_KEY=sk-your-api-key-here
```

### Step 2: Prepare Handbook

Place your employee handbook PDF as `handbook.pdf` in the project root directory.

### Step 3: Launch Application

```bash
streamlit run app.py
```

The application will:
- First run: Process PDF and create vector store (~30 seconds)
- Subsequent runs: Load vector store instantly (~1 second)

### Step 4: Ask Questions

1. Enter your question in the text box
2. Click "Submit Question"
3. View the answer and source citations

### Example Questions

**English:**
- How many vacation days do I get?
- What is the remote work policy?
- How do I submit expense reports?
- What health insurance does the company provide?

**Chinese:**
- 我有多少天假期？
- 远程工作政策是什么？
- 如何报销费用？

## 🛠️ Technology Stack

- **Web Framework**: Streamlit
- **LLM Framework**: LangChain
- **Vector Database**: FAISS
- **PDF Processing**: PDFPlumber
- **LLM**: OpenAI GPT-4o-mini (paid mode)
- **Embedding**: Sentence-Transformers all-MiniLM-L6-v2 (free, local)

## 📁 Project Structure

```
handbook-qa-system/
├── app.py                      # Main application (Streamlit UI)
├── config.py                   # Configuration management
├── document_processor.py       # Document processing module
├── qa_engine.py               # Q&A engine
├── setup.py                   # One-click setup script
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── .env                      # Your configuration (not in git)
├── .gitignore                # Git ignore file
├── handbook.pdf              # Your employee handbook
└── cache/                    # Cache directory (auto-created)
    └── vector_store/         # Vector database storage
```

## ⚙️ Configuration

### Environment Variables (.env file)

```bash
# Mode selection: free or paid
MODE=free

# OpenAI API Key (required for paid mode)
OPENAI_API_KEY=your_api_key_here
```

### Getting OpenAI API Key

1. Visit https://platform.openai.com
2. Sign up for an account
3. Go to API Keys page and create a new key
4. Copy the key to your `.env` file

## 💰 Cost Estimation

### Free Mode
- **Cost**: $0/month
- **Answer Quality**: Direct document retrieval
- **Response Speed**: Fast (1-3 seconds)
- **Best For**: Simple lookups, exact information

### Paid Mode
- **Cost**: ~$0.03/month (100 queries)
- **Answer Quality**: AI-summarized, more natural
- **Response Speed**: Medium (2-5 seconds)
- **Best For**: Complex questions, policy interpretation

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "handbook.pdf not found" | Place your PDF in the project root directory |
| API Key error | Check if OPENAI_API_KEY is correctly set in .env |
| Slow first startup | Normal - processing PDF and creating vector store |
| Answer not accurate | Try rephrasing question or switch to paid mode |

## 📝 Changelog

### v1.0.0 (2024-11-23)
- ✅ Initial release
- ✅ Fixed handbook.pdf support
- ✅ Dual mode (free/paid)
- ✅ Language adaptation (English/Chinese)
- ✅ Vector store persistence
- ✅ Source citation
- ✅ Q&A history

## 📄 License

MIT License

## 🤝 Contributing

Issues and Pull Requests are welcome!

---

**Made with ❤️ for better employee onboarding**
