from crewai import Agent
from TravelTools import search_web_tool
#from TravelTools import search_web_tool, web_search_tool
from crewai import LLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import google.generativeai as genai  # Added this import at the top

# def get_llm():
#     api_key = os.getenv('GOOGLE_API_KEY')
#     if not api_key:
#         raise ValueError("Google API key not found in environment variables")
    
#     # Configure the genai library
#     genai.configure(api_key=api_key)
    
#     return ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         google_api_key=api_key,  # Explicitly pass the API key here
#         temperature=0.7,
#         convert_system_message_to_human=True
#     )
from crewai import LLM

def get_llm():
    return LLM(
        provider="google",  # Specify provider explicitly
        model="gemini-pro",
        api_key=os.getenv("GOOGLE_API_KEY"),
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

location_expert = Agent(
    role="Travel Trip Expert",
    goal="Provides travel logistics and essential information.",
    backstory="A seasoned traveler who knows everything about different cities.",
    tools=[search_web_tool],  
    verbose=True,
    max_iter=5,
    llm= get_llm(),   # ChatOpenAI(temperature=0, model="gpt-4o-mini"),
    allow_delegation=False,
)

planner_expert = Agent(
    role="Travel Planning Expert",
    goal="Compiles all gathered information to create a travel plan.",
    backstory="An expert in planning seamless travel itineraries.",
    tools=[search_web_tool],
    verbose=True,
    max_iter=5,
    llm=get_llm(),
    allow_delegation=False,
)
