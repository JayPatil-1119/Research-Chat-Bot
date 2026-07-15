from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import search_tool, wiki_tool, save_tool

# Load environment variables
load_dotenv()


# -----------------------------
# Pydantic Output Schema
# -----------------------------
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


# -----------------------------
# LLM
# -----------------------------
llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.2,
)


# -----------------------------
# Output Parser
# -----------------------------
parser = PydanticOutputParser(pydantic_object=ResearchResponse)


# -----------------------------
# Prompt
# -----------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert research assistant.

Your job is to answer the user's question by using the available tools whenever needed.

Always return the final answer in the following format:

{format_instructions}
""",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(
    format_instructions=parser.get_format_instructions()
)


# -----------------------------
# Tools
# -----------------------------
tools = [
    search_tool,
    wiki_tool,
    save_tool,
]


# -----------------------------
# Agent
# -----------------------------
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)


# -----------------------------
# Agent Executor
# -----------------------------
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)


# -----------------------------
# User Query
# -----------------------------
query = input("What can I help you research?\n> ")


# -----------------------------
# Run Agent
# -----------------------------
response = agent_executor.invoke(
    {
        "query": query,
        "chat_history": [],
    }
)

print("\nRaw Response:\n")
print(response)


# -----------------------------
# Parse Output
# -----------------------------
try:
    structured_response = parser.parse(response["output"])

    print("\nStructured Response\n")
    print(structured_response)

except Exception as e:
    print("\nParsing Error:")
    print(e)

    print("\nModel Output:")
    print(response["output"])