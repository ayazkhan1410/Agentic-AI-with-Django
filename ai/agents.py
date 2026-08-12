from langchain.agents import create_agent

from ai.llms import get_open_ai_models
from ai.tools import get_document_tool, get_documents_tool

llm = get_open_ai_models()


def get_document_agent():
    agent = create_agent(
        model=llm,
        tools=[get_document_tool, get_documents_tool],
        system_prompt=(
            "You are a helpful assistant in managing a user's documents "
            "within this app"
        ),
    )
    return agent
