from langchain.agents import create_agent

from ai.llms import get_open_ai_models
from ai.tools import (
    get_document_tool, get_documents_tool,
    create_document_tool, update_document_tool,
    search_documents_tool, delete_document_tool,
    search_movie_tool, get_movie_details_tool
)
llm = get_open_ai_models()


def get_document_agent(check_pointer=None):
    tools = [
        get_document_tool, get_documents_tool,
        create_document_tool, update_document_tool,
        search_documents_tool, delete_document_tool
    ]
    agent = create_agent(
        model=llm,
        tools=tools,
        name="document_agent",
        system_prompt=(
            "You are a helpful assistant in managing a user's"
            "documents within this app. "
            "If you need to create, update, or search documents, do so."
        ),
        checkpointer=check_pointer,
    )
    return agent


def get_movie_discovery_agent(check_pointer=None):
    tools = [
        search_movie_tool, get_movie_details_tool
    ]
    agent = create_agent(
        model=llm,
        tools=tools,
        name="movie_discovery_agent",
        system_prompt=(
            "You are a helpful assistant in discovering movies based on "
            "a user's query. If you need to search for a movie, do so."
        ),
        checkpointer=check_pointer,
    )
    return agent
