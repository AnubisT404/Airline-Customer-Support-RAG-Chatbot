# Airline Customer Support RAG Chatbot

This project is an **AI-powered customer support chatbot**, leveraging **Retrieval-Augmented Generation (RAG)** and **LangGraph** to provide airline-related assistance. The chatbot can handle:
- Flight information lookup
- Ticket updates & cancellations
- Hotel & car rental bookings
- Excursion recommendations
- General customer inquiries

The chatbot integrates **LLM-based reasoning with structured and unstructured data retrieval**, ensuring accurate responses by fetching real-time airline policies and booking details.

---

## Installation

Install the requirements:
```
pip install -r requirements.txt
```

Create a `.env` file in the project root and add:
```
OPEN_AI_API_KEY=your_openai_api_key_here
TAVILY_SEARCH_KEY=your_tavily_search_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

Then, download files and preprocess them:
```
python3 data_preparation/download_data.py
python3 data_preparation/prepare_vector_db.py
```

Run the interface:
```
python3 src/utils/app.py
```
