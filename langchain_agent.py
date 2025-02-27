import os
import requests
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set your OpenAI API key in the environment variable OPENAI_API_KEY.")


# Define tool functions that query our FastAPI backend.
def query_total_passengers():
    response = requests.get("http://127.0.0.1:8000/total_passengers").json()
    return f"Total Passengers: {response.get('total_passengers', 'unknown')}"


def query_survival_rate():
    response = requests.get("http://127.0.0.1:8000/survival_rate").json()
    return f"Survival Rate: {response.get('survival_rate', 'unknown'):.2f}%"


def query_percentage_male():
    response = requests.get("http://127.0.0.1:8000/percentage_male").json()
    return f"Percentage of Male Passengers: {response.get('percentage_male', 'unknown'):.2f}%"


def query_average_fare():
    response = requests.get("http://127.0.0.1:8000/average_fare").json()
    return f"Average Ticket Fare: ${response.get('average_fare', 'unknown'):.2f}"


def query_embarked():
    response = requests.get("http://127.0.0.1:8000/embarked").json()
    embarked_info = response.get("embarked", {})
    return f"Embarkation Counts: {embarked_info}"


# Define tools for the agent.
tools = [
    Tool(
        name="Total Passengers",
        func=query_total_passengers,
        description="Returns the total number of passengers on the Titanic."
    ),
    Tool(
        name="Survival Rate",
        func=query_survival_rate,
        description="Returns the survival rate (in percent) of Titanic passengers."
    ),
    Tool(
        name="Percentage Male",
        func=query_percentage_male,
        description="Returns the percentage of male passengers on the Titanic."
    ),
    Tool(
        name="Average Fare",
        func=query_average_fare,
        description="Returns the average ticket fare for Titanic passengers."
    ),
    Tool(
        name="Embarkation Info",
        func=query_embarked,
        description="Returns a dictionary of passenger counts by embarkation port."
    )
]

# LangChain LLM using ChatOpenAI.
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)


# Create an agent using the Zero-Shot React Description strategy.
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

def query_titanic(question: str) -> str:
    """Given a natural language question, let the LangChain agent determine which tool to call."""
    return agent.run(question)
