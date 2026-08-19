from langgraph_supervisor import create_supervisor

from ai.agents import get_document_agent, get_movie_discovery_agent
from ai.llms import get_open_ai_models


def get_supervisor(checkpointer=None):
    movie_discovery_agent = get_movie_discovery_agent()
    document_agent = get_document_agent()
    llm = get_open_ai_models()

    supervisor = create_supervisor(
        [movie_discovery_agent, document_agent],
        model=llm,
        prompt=(
            "You are a team supervisor managing a movie discovery agent and a "
            "document agent. "
            "For movie discovery, use movie_discovery_agent. "
            "For document management, use document_agent."
        ),
    )
    return supervisor.compile(checkpointer=checkpointer)
