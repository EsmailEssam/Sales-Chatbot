# Sales Chatbot

An advanced AI-powered sales assistant built with LangGraph and FastAPI. This chatbot helps users discover, search, and learn about products through natural, conversational interactions. It supports product recommendations, price-based queries, and integration with external data sources, making it ideal for e-commerce and customer support scenarios.

## Features

- Search for products by name, category, or specific needs
- Query products by price (lowest, highest, or within a range)
- Get personalized product recommendations using natural language
- Integrate with external knowledge bases and APIs
- User-friendly conversational interface for product inquiries
- Robust logging and error handling
- Modular, extensible architecture for easy customization

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/sales-chatbot.git
cd sales-chatbot
```

2. **Create a virtual environment:**
```bash
python -m venv venv
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -e .
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your API keys and configuration
```

## Usage

### 1. Run the Streamlit App (GUI)
To launch the graphical user interface for interactive product search:
```bash
python app.py
```

### 2. Run the FastAPI Server (API)
To start the backend API server for integration with other services:
```bash
uvicorn main_api:app --reload --host 0.0.0.0 --port 5000
```

### 3. Run the Chatbot from the Command Line
To interact with the chatbot via the terminal:
```bash
python main.py
```


### 4. Example Queries
- "Show me products for hair loss"
- "What are the cheapest products available?"
- "Find skincare products for dry skin"
- "What products are in the Hair Care category?"


## Run with Docker Compose

You can run the entire project (API, dependencies, etc.) using Docker Compose for easy deployment and isolation.

1. **Build and start the services:**
```bash
docker compose up --build
```

2. **Access the API:**
- By default, the FastAPI server will be available at:  
  http://localhost:5000

3. **Stop the services:**
```bash
docker compose down
```

> Make sure you have Docker and Docker Compose installed on your system.

## الهيكل العام للمشروع (Project Structure)

```
sales-chatbot/
├── app.py
├── main.py
├── main_api.py
├── compose.yml
├── Dockerfile
├── requirements.txt
├── setup.py
├── langgraph.json
├── .gitignore
├── .dockerignore
├── README.md
├── DataBase/
│   └── checkpoint.sqlite (قاعدة بيانات SQLite لتخزين البيانات)
├── Dataset/
│   └── products.json (قاعدة بيانات المنتجات)
├── assets/
│   └── salles_chat_bot.postman_collection.json (ملف Postman لاختبار الـ API)
├── logs/
│   └── app.log (سجل الأحداث والأخطاء)
├── notebook/
│   ├── *.ipynb (دفاتر Jupyter للتجارب والتحليل)
│   ├── products.csv, processed_products.csv (ملفات بيانات معالجة)
│   └── products.json (نسخة من بيانات المنتجات)
├── prompts/
│   ├── output_formatter_prompt.txt (قالب موجه لتنسيق المخرجات)
│   └── sales_agent_prompt.txt (قالب موجه لوكيل المبيعات)
├── routes/
│   ├── __init__.py
│   ├── base_router.py (الراوتر الأساسي لتجميع المسارات)
│   └── chat_route.py (مسارات الدردشة الخاصة بالبوت)
├── src/
│   ├── __init__.py
│   ├── graph.py (تعريف الرسم البياني لتدفق المحادثة)
│   ├── helper/
│   │   ├── __init__.py
│   │   ├── config.py (إعدادات المشروع)
│   │   └── get_the_data_from_the_end_point.py (جلب البيانات من نقطة النهاية)
│   ├── graph_blocks/
│   │   ├── __init__.py
│   │   ├── nodes.py (تعريف العقد في الرسم البياني)
│   │   ├── state.py (إدارة حالة المحادثة)
│   │   ├── llm_blocks/
│   │   │   ├── __init__.py
│   │   │   ├── base.py (الأساسيات للتكامل مع نماذج اللغة)
│   │   │   ├── output_formatter.py (تنسيق مخرجات النموذج)
│   │   │   └── sales_agent.py (وكيل المبيعات الذكي)
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── df_tools.py (أدوات التعامل مع البيانات)
│   ├── df_manager/
│   │   ├── __init__.py
│   │   ├── df_manager.py (إدارة وتحليل البيانات)
│   │   └── df_manager_helpers/
│   │       ├── __init__.py
│   │       ├── convert_json_to_df.py (تحويل JSON إلى DataFrame)
│   │       └── preprocess_df.py (معالجة البيانات قبل التحليل)
│   ├── log_manager/
│   │   ├── __iniy__.py
│   │   └── log_manager.py (إدارة السجلات)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── output_formatter.py (مخطط تنسيق المخرجات)
│   │   ├── products_from_end_point_schema.py (مخطط بيانات المنتجات من نقطة النهاية)
│   │   ├── end_point_json_schema.py (مخطط بيانات نقطة النهاية)
│   │   ├── enums/
│   │   │   ├── __init__.py
│   │   │   ├── llm_enums.py (تعدادات خاصة بنماذج اللغة)
│   │   │   └── api_errors_message.py (رسائل أخطاء الـ API)
│   │   └── routes_schemes/
│   │       ├── __init__.py
│   │       └── chat_request.py (مخطط طلبات الدردشة)
│   └── utils/
│       ├── __init__.py
│       └── metrics.py (حساب مقاييس الأداء)
├── tests/
│   ├── __init__.py
│   ├── test_main.py (اختبارات نقطة الدخول الرئيسية)
│   ├── test_df_manager/
│   │   ├── __init__.py
│   │   ├── test_df_manager.py (اختبارات إدارة البيانات)
│   │   └── test_df_manager_helpers/
│   │       ├── __init__.py
│   │       └── test_convert_json_to_df.py (اختبار تحويل JSON إلى DataFrame)
│   └── test_helper/
│       ├── __init__.py
│       └── test_get_the_data_from_the_end_point.py (اختبار جلب البيانات من نقطة النهاية)
```

### شرح الملفات والمجلدات الرئيسية:

- **app.py**: تطبيق Streamlit لواجهة المستخدم الرسومية.
- **main.py**: نقطة تشغيل المشروع الأساسية (تشغيل البوت).
- **main_api.py**: تعريف واجهات برمجة التطبيقات (API) باستخدام FastAPI.
- **compose.yml, Dockerfile**: ملفات إعداد الحاويات (Docker) لتسهيل النشر.
- **requirements.txt, setup.py**: متطلبات المشروع وتعريف الحزمة.
- **langgraph.json**: إعدادات خاصة بتكامل LangGraph.
- **DataBase/**: يحتوي على قاعدة بيانات SQLite لتخزين البيانات.
- **Dataset/**: ملفات وبيانات المنتجات المستخدمة في التدريب أو التشغيل.
- **assets/**: ملفات مساعدة مثل Postman collection لاختبار الـ API.
- **logs/**: ملفات السجلات لتتبع الأخطاء والأحداث.
- **notebook/**: دفاتر Jupyter للتجارب وتحليل البيانات.
- **prompts/**: قوالب موجهات (prompts) لنماذج اللغة.
- **routes/**: تعريف مسارات الـ API الخاصة بالدردشة.
- **src/**: الكود الأساسي للمشروع ويحتوي على:
    - **helper/**: دوال مساعدة مثل جلب البيانات من نقطة النهاية.
    - **graph_blocks/**: مكونات الرسم البياني للمحادثة (عقد، حالات، تكامل مع LLM، أدوات).
    - **df_manager/**: إدارة وتحليل البيانات وتحويلها.
    - **log_manager/**: إدارة السجلات وتسجيل الأحداث.
    - **schemas/**: مخططات البيانات (Data Schemas) والتعدادات.
    - **utils/**: دوال مساعدة لحساب المقاييس.
- **tests/**: اختبارات وحدات الكود لضمان الجودة.


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

