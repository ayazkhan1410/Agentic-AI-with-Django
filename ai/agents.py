from langchain.agents import create_agent

from ai.llms import get_open_ai_models
from ai.tools import (
    get_document_tool, get_documents_tool,
    create_document_tool
)
llm = get_open_ai_models()


def get_document_agent(check_pointer=None):
    tools = [
        get_document_tool, get_documents_tool,
        create_document_tool
    ]
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "You are a helpful assistant in managing a user's documents "
            "within this app"
        ),
        checkpointer=check_pointer,
    )
    return agent
