# AI Chatbot with FastAPI and Streamlit

This project is an AI chatbot application featuring a backend built with FastAPI and a user interface created with Streamlit. It leverages Langchain to interact with language models from Groq and OpenAI, and can use Tavily Search for web-enhanced responses.

## Prerequisites

*   Python 3.13
*   `pipenv` (recommended for managing dependencies) or `pip`

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and Activate Virtual Environment:**

    *   **Using `pipenv` (recommended):**
        ```bash
        pipenv shell
        ```
        This command will create a virtual environment if one doesn't exist and activate it.

    *   **Using `venv`:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
        ```

3.  **Install Dependencies:**

    *   **Using `pipenv`:**
        ```bash
        pipenv install
        ```
        If you also want to install development dependencies (though none are listed in the current `Pipfile`):
        ```bash
        pipenv install --dev
        ```

    *   **Using `pip` (after `requirements.txt` is created):**
        ```bash
        pip install -r requirements.txt
        ```

4.  **Set Up Environment Variables:**
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Open the `.env` file and add your API keys:
        ```
        GROQ_API_KEY="your_groq_api_key"
        OPENAI_API_KEY="your_openai_api_key"
        TAVILY_API_KEY="your_tavily_api_key"
        ```
        *Note: The application uses `python-dotenv` to load these variables, so ensure it's installed if not using `pipenv` which handles `.env` files automatically.*

## Running the Application

1.  **Run the Backend Server:**
    Open a terminal, ensure your virtual environment is activated, and run:
    ```bash
    python backend.py
    ```
    Alternatively, you can use Uvicorn for more control (FastAPI's recommended ASGI server):
    ```bash
    uvicorn backend:app --host 127.0.0.1 --port 9999 --reload
    ```
    The backend server will start, typically on `http://127.0.0.1:9999`.

2.  **Run the Frontend Application:**
    Open another terminal, ensure your virtual environment is activated, and run:
    ```bash
    streamlit run forntend.py
    ```
    The Streamlit application will open in your web browser, usually at `http://localhost:8501`.

## API Endpoint

The backend exposes a `POST` endpoint for chat interactions:

*   **URL:** `http://127.0.0.1:9999/chat`
*   **Method:** `POST`
*   **Body (JSON):**
    ```json
    {
      "model_name": "llama-3.3-70b-versatile", // or other allowed models
      "model_provider": "Groq", // or "OpenAI"
      "system_prompt": "You are a helpful assistant.",
      "messages": ["Hello, how are you?"],
      "allow_search": true // or false
    }
    ```

You can explore and test the API using the Swagger UI documentation available at `http://127.0.0.1:9999/docs` when the backend server is running.
