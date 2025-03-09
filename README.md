# Full-Stack RAG Application

**RAG (Retrieval-Augmented Generation)** application with:  
- **FastAPI** backend  
- **React** frontend  
- **Ollama** for open-source LLM support  
- **Qdrant** for vector database  

---

## Features
✅ Ask questions and get answers with cited sources  
✅ Index websites into the vector database  
✅ Open-source LLM integration (via Ollama)  
✅ REST API for chat and data ingestion  

---

## Prerequisites
1. **Python 3.10+**  
2. **Node.js 18+**  
3. **Ollama** installed ([download here](https://ollama.ai/))  
4. **Qdrant** running (local/cloud instance)  

---

## Setup Instructions

### 1. Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in QDRANT_URL, QDRANT_API_KEY, and OLLAMA_MODEL_NAME
```
### 2. Frontend (React)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```
### 3. Start Ollama
```bash
# Pull your desired model (e.g., llama2)
ollama pull llama2

# Start Ollama service
ollama serve
```
## Environment Variables
### Backend (.env)
```bash
QDRANT_URL=
QDRANT_API_KEY=your_qdrant_api_key
OLLAMA_MODEL_NAME=llama2  # Or any Ollama model name
```
### 
