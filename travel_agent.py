from crewai import Agent
from TravelTools import search_web_tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_llm():
    # Get API key from environment variable
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("Google API key not found in environment variables")
    
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=api_key,
        temperature=0.7
    )

# Agents
guide_expert = Agent(
    role="City Local Guide Expert",
    goal="Provides information on things to do in the city based on user interests.",
    backstory="A local expert passionate about sharing city experiences.",
    tools=[search_web_tool],
    verbose=True,
    max_iter=5,
    llm=get_llm(),
    allow_delegation=False,
)

# ... rest of your agents remain the same, just update the llm=get_llm() for each ...