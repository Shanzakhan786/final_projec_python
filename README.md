# CAG Project API: Chat with Your PDF

The CAG Project is an intelligent API platform that allows users to interact with and query the contents of PDF documents using advanced Large Language Models (LLMs) via FastAPI. It enables seamless uploading, processing, and conversational querying of PDF files, making document understanding and data management easy and efficient.

> **What does CAG mean?**
>
> **CAG** stands for **Conversational AI Gateway**. It is a backend system that acts as a gateway for interacting with documents (like PDFs) using conversational AI. The CAG Project enables users to upload documents, extract their content, and ask questions about them through a chat-like API interface powered by Google Gemini LLM.

## Project Description
CAG (Conversational AI Gateway) Project provides a robust backend for document-based AI chat. Users can upload PDF files, extract and store their text, and then ask questions about the content. The system leverages Google Gemini LLM to generate context-aware answers, making it ideal for academic, business, or research use cases where understanding and extracting insights from documents is essential.

## Features
- **Chat with PDF documents:** Upload PDFs and ask questions about their content.
- **Query PDF content using LLM:** Uses Google Gemini LLM to answer user queries based on the uploaded document's text.
- **Data management endpoints:** Upload, update, delete, and list PDF data by UUID.
- **Interactive API documentation:** Swagger UI for easy API exploration and testing.

## How It Works
- **main.py:** The entry point. Sets up the FastAPI app, loads routers, and provides a web welcome page and API docs.
- **src/routers/data_handler.py:** Contains all main API endpoints for uploading, updating, querying, deleting, and listing PDF data. Handles file storage, text extraction, and LLM query routing.
- **src/utils/pdf_processing.py:** Extracts text from uploaded PDF files using PyPDF.
- **src/utils/llm_client.py:** Connects to Google Gemini LLM, sending user queries and PDF context, and returns AI-generated answers.
- **src/utils/data_store.py:** Provides a simple in-memory data store for associating extracted text with UUIDs.
- **requirements.txt:** Lists all required Python packages, including FastAPI, Uvicorn, PyPDF, and Google GenerativeAI.
- **.env:** Stores your Google Gemini API key as `GEMINI_API_KEY` (required for LLM features).

## Getting Started

### Prerequisites
- Python 3.8+

### Installation
1. Clone the repository or download the source code.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Google Gemini API key in a `.env` file:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

### Running the API
Start the FastAPI server with Uvicorn:
```bash
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) for the welcome page.
API documentation is at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Project Structure
- `main.py`: Main FastAPI application.
- `requirements.txt`: Python dependencies.
- `src/routers/data_handler.py`: API endpoints for PDF and data management.
- `src/utils/pdf_processing.py`: PDF text extraction logic.
- `src/utils/llm_client.py`: LLM (Google Gemini) integration.
- `src/utils/data_store.py`: In-memory data storage.
- `.env`: API key configuration.

## Notes
- All PDF content is processed and stored in-memory (not persistent).
- The project is modular—extend routers and utils for more features.
- For production, consider persistent storage and secure API key management.

---

*Developed for the CAG Project: Making document chat and AI-powered PDF understanding accessible and easy.*
