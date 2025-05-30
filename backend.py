# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup Pydantic Model (Schema Validation)
from pydantic import BaseModel
from typing import List


class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


#Step2: Setup AI Agent from FrontEnd Request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ai_agent import get_response_from_ai_agent

# Allowed model names
ALLOWED_MODEL_NAMES = ["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]
ALLOWED_PROVIDERS = ["Groq", "OpenAI"]

# Initialize FastAPI app
app = FastAPI(
    title="LangGraph AI Agent",
    description="API for interacting with AI models using LangGraph",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request.
    
    - **model_name**: The name of the model to use (e.g., 'llama-3.3-70b-versatile')
    - **model_provider**: The provider of the model ('Groq' or 'OpenAI')
    - **system_prompt**: Initial instructions for the AI
    - **messages**: List of message strings from the user
    - **allow_search**: Whether to enable web search
    """
    try:
        # Input validation
        if not request.messages:
            raise HTTPException(status_code=400, detail="Messages cannot be empty")
            
        if request.model_name not in ALLOWED_MODEL_NAMES:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid model name. Please choose from: {', '.join(ALLOWED_MODEL_NAMES)}"
            )
            
        if request.model_provider not in ALLOWED_PROVIDERS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider. Please choose from: {', '.join(ALLOWED_PROVIDERS)}"
            )
        
        # Process the request
        response = get_response_from_ai_agent(
            llm_id=request.model_name,
            query=request.messages,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt,
            provider=request.model_provider
        )
        
        return {"response": response}
        
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except Exception as e:
        # Log the error and return a 500 response
        print(f"Error in chat_endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request. Please try again later."
        )

#Step3: Run app & Explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)