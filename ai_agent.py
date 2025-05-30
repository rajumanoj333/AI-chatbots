# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup API Keys for Groq, OpenAI and Tavily
import os

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

#Step2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

openai_llm=ChatOpenAI(model="gpt-4o-mini")
groq_llm=ChatGroq(model="llama-3.3-70b-versatile")

search_tool=TavilySearchResults(max_results=2)

#Step3: Setup AI Agent with Search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt="Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    try:
        # Initialize the appropriate LLM
        if provider == "Groq":
            llm = ChatGroq(model=llm_id)
        elif provider == "OpenAI":
            llm = ChatOpenAI(model=llm_id)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        # Initialize tools if search is enabled
        tools = [TavilySearchResults(max_results=2)] if allow_search else []
        
        # Create the agent
        agent = create_react_agent(
            model=llm,  # Changed from llm=llm to model=llm
            tools=tools
        )
        
        # Prepare the initial state with system and user messages
        state = {
            "messages": [
                {"role": "system", "content": system_prompt},
                *[{"role": "user", "content": msg} for msg in query]
            ]
        }
        
        # Get the response
        response = agent.invoke(state)
        messages = response.get("messages", [])
        
        # Extract AI responses
        ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
        
        # Return the last AI message or a default response
        return ai_messages[-1] if ai_messages else "I'm sorry, I couldn't generate a response."
        
    except Exception as e:
        # Log the error and return a user-friendly message
        print(f"Error in get_response_from_ai_agent: {str(e)}")
        return f"An error occurred while processing your request: {str(e)}"