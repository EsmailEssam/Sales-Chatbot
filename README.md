# Sales Chatbot

An AI-powered sales assistant built with LangGraph that helps users find and learn about products through natural conversation.

## Features

- Product search by name, category, or specific concerns
- Price-based queries (lowest/highest price, price range)
- Natural language understanding for product recommendations
- Integration with external knowledge bases
- Conversational interface for product inquiries

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sales-chatbot.git
cd sales-chatbot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## Usage

1. Start the chatbot:
```bash
python main.py
```

2. Interact with the chatbot using natural language queries like:
- "Show me products for hair loss"
- "What are the cheapest products available?"
- "Find skincare products for dry skin"
- "What products are in the Hair Care category?"

## Project Structure

```
sales-chatbot/
├── app.py                # streamlit application
├── main.py              # Entry point
├── main_api.py          # API endpoints
├── Dataset/             # Data files
│   └── products.json    # Product database
├── src/             # Core src
│   ├── df_manager/      # DataFrame management
│   ├── graph_blocks/    # LangGraph components
│   ├── llm_blocks/      # LLM integration
│   ├── helper/          # Utility functions
│   ├── log_manager/     # Logging system
│   └── schemas/         # Data schemas
├── routes/              # API routes
├── assets/              # Project assets
├── prompts/             # LLM prompt templates
├── notebook/            # Jupyter notebooks
└── tests/               # Test files
    ├── test_df_manager/ # DataFrame tests
    └── test_helper/     # Helper function tests
```

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## Run fast api server :

```bash
uvicorn main_api:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection:

Download the psotman collection from [assets\salles_chat_bot.postman_collection.json](assets\salles_chat_bot.postman_collection.json)


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Uses LangChain for LLM integration 


في الفيرجن ده انا ضفت نود جديده عشان تخرح الاوتبت في جسون زي ما احنا عاوزين واشتغلت بالفعل وظبط شويه حاجات في الاستركشر بتاع لمشروع وال وان تيست دلوقتي هو الي شغال