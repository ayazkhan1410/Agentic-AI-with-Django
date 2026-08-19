# Agentic AI with Django

A Django REST API that uses **LangChain**, **LangGraph**, and a **supervisor** to route questions between two specialists:

- **Document agent** — create, list, search, update, and delete user documents
- **Movie discovery agent** — search movies and fetch details via [TMDB](https://www.themoviedb.org/)

Chat with the document agent over HTTP (`POST /api/chat/`), or run the full supervisor from Jupyter notebooks.

## Features

- Document CRUD scoped to an owner (`user_id` in agent config)
- REST API for listing and fetching documents
- Natural-language tools for documents and movies
- Multi-agent **supervisor** that hands off to the right specialist
- Optional **checkpointer** (conversation memory via `thread_id`)
- Jupyter notebooks that walk through each step

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 6, Django REST Framework |
| AI | LangChain, LangGraph, langgraph-supervisor, LangChain OpenAI |
| Movies | TMDB API (`tmbd/client.py`) |
| Config | python-decouple |
| Database | SQLite (default) |
| Notebooks | Jupyter |

## Project Structure

```
Agentic-Ai-Django/
├── aiengine/              # Django project (settings, URLs)
├── agents/                # Document app (models, views, serializers, admin)
├── ai/                    # Agents, tools, LLM, supervisor
│   ├── llms.py            # OpenAI ChatOpenAI setup
│   ├── tools.py           # Document + movie tools
│   ├── agents.py          # document_agent and movie_discovery_agent
│   └── supervisor.py      # Routes work between the two agents
├── tmbd/                  # TMDB HTTP client
├── notebook/              # Tutorials + Django bootstrap (setup.py)
├── manage.py
├── requirements.txt
└── .env.example
```

## Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key (a model your account can use)
- TMDB read access token (for movie search)

### Installation

```bash
git clone <your-repo-url>
cd Agentic-Ai-Django

python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

pip install -r requirements.txt

cp .env.example .env
# Fill in OpenAI + TMDB values in .env

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin: `http://127.0.0.1:8000/admin/`

### Environment Variables

Copy `.env.example` to `.env`. **Do not commit `.env`.**

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key (required for chat/agents) |
| `OPENAI_ORGANIZATION` | OpenAI org ID (`org-...`), optional |
| `OPENAI_MODEL` | Model name your account supports |
| `MOVIE_DB_API_KEY` | TMDB API key |
| `MOVIE_DB_READ_ACCESS_TOKEN` | TMDB Bearer token (used by the client) |
| `SEARCH_MOVIE_URL` | TMDB search endpoint |
| `MOVIE_DETAILS_URL` | TMDB details URL with `{movie_id}` placeholder |

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/retrieve-document/` | List all documents |
| `GET` | `/api/retrieve-single-document/<id>/` | Get one active document |
| `POST` | `/api/chat/` | Chat with the **document** agent |

### Chat example

```http
POST /api/chat/
Content-Type: application/json

{
  "message": "Create a document titled Meeting Notes with content Team sync summary"
}
```

```json
{
  "message": "Chat response generated successfully",
  "user": { "id": 1, "username": "admin" },
  "agent_reply": "I've created your document titled Meeting Notes."
}
```

Example prompts:

- `"List my documents"`
- `"Search documents about Meeting Notes"`
- `"Update document 20 title to The Dark Knight"`
- `"Create a document titled API Notes with content REST details"`

The chat view currently uses `get_document_agent()`. Movie routing is available through the **supervisor** in notebooks (`ai/supervisor.py`).

## Agents

| Agent | Name | Role |
|-------|------|------|
| Document | `document_agent` | Manage documents in Django |
| Movie discovery | `movie_discovery_agent` | Search TMDB and get movie details |
| Supervisor | `get_supervisor()` | Decides which specialist to call |

### Document tools

| Tool | Description |
|------|-------------|
| `get_document` | One document by ID (owner-scoped) |
| `get_documents` | Recent documents (`limit` capped) |
| `create_document` | Create a document for the user |
| `update_document` | Update title and/or content |
| `search_documents` | Search title/content (`icontains`) |
| `delete_document` | Delete a user's document |

### Movie tools

| Tool | Description |
|------|-------------|
| `search_movie_tool` | Search TMDB by query |
| `get_movie_details_tool` | Details for one TMDB movie ID |

Tools read `user_id` from LangGraph config (not from the message body):

```python
agent.invoke(
    {"messages": [{"role": "user", "content": message}]},
    {"configurable": {"user_id": user.id, "thread_id": "chat-1"}},
)
```

- **`user_id`** — whose documents to use  
- **`thread_id`** — conversation id (needed for checkpointer memory)

### Supervisor + memory

```python
from langgraph.checkpoint.memory import InMemorySaver
from ai.supervisor import get_supervisor

supervisor = get_supervisor(checkpointer=InMemorySaver())
result = supervisor.invoke(
    {"messages": [{"role": "user", "content": "Find The Dark Knight and save it as a document"}]},
    {"configurable": {"user_id": 1, "thread_id": "chat-1"}},
)
print(result["messages"][-1].content)
```

Print only the last message in notebooks so the cell output stays small.

## Notebooks

Run **cell 0** first in each notebook (`notebook/setup.py` bootstraps Django).

| Notebook | Topic |
|----------|--------|
| `1-hello.ipynb` | Intro |
| `2-django-user-perms.ipynb` | Users, permissions, documents |
| `3-langgraph-django-tool.ipynb` | Django tools vs LangChain `.invoke()` |
| `4-verifiy-llm-django.ipynb` | OpenAI / LLM setup |
| `5-get-started-with-agents.ipynb` | Document agent basics |
| `6-agent-memeory.ipynb` | Agent memory (checkpointer) |
| `7-create-document.ipynb` | Create documents via agent |
| `8-update-document.ipynb` | Update documents |
| `9-search-document.ipynb` | Search documents |
| `10-tmdb-api-client.ipynb` | TMDB client |
| `11-movie-discovery-ai-agent.ipynb` | Movie discovery agent |
| `12-multi-agent-supervisor.ipynb` | Supervisor (documents + movies) |
