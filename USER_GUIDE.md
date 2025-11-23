# User Guide - Employee Handbook Q&A System

## Table of Contents
1. [Getting Started](#getting-started)
2. [Using the Application](#using-the-application)
3. [Understanding Modes](#understanding-modes)
4. [Tips for Best Results](#tips-for-best-results)
5. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Your employee handbook as `handbook.pdf`
- (Optional) OpenAI API key for paid mode

### Installation

**Option 1: One-Click Setup**
```bash
python setup.py
```

**Option 2: Manual Setup**
```bash
pip install -r requirements.txt
streamlit run app.py
```

### First Launch

1. The application will automatically process `handbook.pdf`
2. This takes about 30 seconds on first run
3. A vector store is created and saved for future use
4. Subsequent launches are instant (~1 second)

## Using the Application

### Main Interface

The application has three main areas:

1. **Sidebar** (left)
   - Mode selection (Free/Paid)
   - Usage statistics
   - Clear cache button

2. **Question Input** (center)
   - Text box for your question
   - Submit button

3. **Results Area** (below)
   - AI-generated answer
   - Source citations with page numbers
   - Q&A history

### Asking Questions

1. **Type your question** in plain language
   - English: "How many vacation days do I get?"
   - Chinese: "我有多少天假期？"

2. **Click "Submit Question"**

3. **Review the answer**
   - The AI will respond in the same language as your question
   - Source citations show which page the information comes from

### Example Questions

**Policy Questions:**
- What is the remote work policy?
- Can I work from home on Fridays?
- What are the core working hours?

**Benefits Questions:**
- How many vacation days do I get?
- What health insurance does the company provide?
- Is there a professional development budget?

**Procedure Questions:**
- How do I submit expense reports?
- What is the process for requesting time off?
- How do I report a workplace issue?

## Understanding Modes

### Free Mode

**How it works:**
- Retrieves relevant sections from the handbook
- Returns document content directly
- No AI summarization

**Best for:**
- Quick lookups
- Finding exact policy text
- When you don't have an API key

**Pros:**
- ✅ Completely free
- ✅ Fast responses (1-3 seconds)
- ✅ No API key needed

**Cons:**
- ❌ Returns raw document text
- ❌ May include irrelevant information
- ❌ Less natural language

### Paid Mode

**How it works:**
- Retrieves relevant sections from the handbook
- AI summarizes and synthesizes the information
- Provides natural language answers

**Best for:**
- Complex questions
- Policy interpretation
- When you want concise, clear answers

**Pros:**
- ✅ Natural, easy-to-understand answers
- ✅ Summarizes multiple policy sections
- ✅ Better at understanding context

**Cons:**
- ❌ Requires OpenAI API key
- ❌ Small cost (~$0.03/100 questions)
- ❌ Slightly slower (2-5 seconds)

### Switching Modes

1. Open the sidebar
2. Select your preferred mode
3. The system automatically reinitializes
4. Start asking questions

## Tips for Best Results

### Writing Good Questions

**✅ DO:**
- Be specific: "How many vacation days do I get in my first year?"
- Use natural language: "Can I work remotely on Fridays?"
- Ask one thing at a time: "What is the dress code?"

**❌ DON'T:**
- Be too vague: "Tell me about benefits"
- Ask multiple questions: "What about vacation, sick days, and holidays?"
- Use jargon unnecessarily: "What's the PTO accrual methodology?"

### Getting Better Answers

1. **Rephrase if needed**: If the answer isn't helpful, try asking differently
2. **Check sources**: Review the cited page numbers for full context
3. **Use paid mode for complex questions**: Policy interpretation works better with AI
4. **Use free mode for exact quotes**: When you need the exact policy wording

### Language Support

- **English questions** → English answers
- **Chinese questions** → Chinese answers
- The AI automatically detects and matches your language

## Troubleshooting

### Common Issues

**"handbook.pdf not found"**
- Solution: Place your PDF file in the project root directory
- File must be named exactly `handbook.pdf`

**"API Key not found" (Paid Mode)**
- Solution: Set `OPENAI_API_KEY` in your `.env` file
- Format: `OPENAI_API_KEY=sk-your-key-here`

**Slow first startup**
- This is normal - the system is processing the PDF
- Creates a vector store for fast future access
- Only happens once

**Answer not relevant**
- Try rephrasing your question
- Be more specific
- Switch to paid mode for better understanding

**"No relevant information found"**
- The handbook may not contain this information
- Try related keywords
- Check if the topic is covered in the handbook

### Clearing Cache

If you experience issues:
1. Click "Clear Cache" in the sidebar
2. Restart the application
3. The system will reprocess the handbook

### Getting Help

If problems persist:
1. Check the error message in the application
2. Review the console/terminal output
3. Ensure all dependencies are installed
4. Verify your `.env` configuration

---

**Need more help?** Contact your system administrator or IT support.
