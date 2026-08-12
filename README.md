# Agentic AI with Django

A Django REST API project that combines **Django**, **LangChain**, and **LangGraph** to build an AI agent for managing user documents. Users can chat with the agent to list, retrieve, and create documents scoped to their account.

## Features

- **Document management** — Document model with owner, title, content, and active status
- **REST API** — List and retrieve documents via Django REST Framework
- **AI chat agent** — Natural-language interface powered by OpenAI and LangGraph
- **Agent tools** — Get one document, list documents, and create documents from chat
- **Per-user isolation** — Tools filter documents by `user_id` from agent config
- **Jupyter notebooks** — Step-by-step tutorials for Django, tools, LLMs, agents, and memory

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 6, Django REST Framework |
| AI / Agents | LangChain, LangGraph, LangChain OpenAI |
| Config | python-decouple |
| Database | SQLite (default) |
| Notebooks | Jupyter |

## Project Structure

```
Agentic-Ai-Django/
├── aiengine/          # Django project settings & URLs
├── agents/            # Document app (models, views, serializers, admin)
├── ai/                # LLM, tools, and agent definitions
│   ├── llms.py        # OpenAI chat model setup
│   ├── tools.py       # Document tools for the agent
│   └── agents.py      # LangGraph agent factory
├── notebook/          # Learning notebooks + Django bootstrap (setup.py)
├── manage.py
├── requirements.txt
└── .env.example
```

## Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key with access to your chosen model

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Agentic-Ai-Django

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and OPENAI_MODEL

# Run migrations
python manage.py migrate

# Create a superuser (for admin and testing)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key (required) |
| `OPENAI_ORGANIZATION` | OpenAI org ID (`org-...`), optional |
| `OPENAI_MODEL` | Model name, e.g. `gpt-4o-mini` |

See `.env.example` for a template. **Never commit `.env` to Git.**

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/retrieve-document/` | List all documents |
| `GET` | `/api/retrieve-single-document/<id>/` | Get one active document |
| `POST` | `/api/chat/` | Chat with the document agent |

### Chat Example

```http
POST /api/chat/
Content-Type: application/json

{
  "message": "Create a document titled Meeting Notes with content Team sync summary"
}
```

**Response:**

```json
{
  "message": "Chat response generated successfully",
  "user": { "id": 1, "username": "admin" },
  "agent_reply": "I've created your document titled Meeting Notes."
}
```

Example prompts:

- `"List my documents"`
- `"What is the title of document id 3?"`
- `"Create a document titled API Notes with content REST endpoint details"`

## Agent & Tools

The agent is built with `create_agent` (LangChain) and uses three tools:

| Tool | Description |
|------|-------------|
| `get_document` | Fetch one document by ID (owner-scoped) |
| `get_documents` | Fetch last 5 active documents for the user |
| `create_document` | Create a new document for the user |

Tools receive `user_id` via LangGraph config:

```python
agent.invoke(
    {"messages": [{"role": "user", "content": message}]},
    {"configurable": {"user_id": user.id, "thread_id": "..."}},
)
```

## Notebooks

| Notebook | Topic |
|----------|--------|
| `1-hello.ipynb` | Intro |
| `2-django-user-perms.ipynb` | Users, permissions, documents |
| `3-langgraph-django-tool.ipynb` | Django tools + LangChain `.invoke()` |
| `4-verifiy-llm-django.ipynb` | OpenAI / LLM setup |
| `5-get-started-with-agents.ipynb` | LangGraph agent basics |
| `6-agent-memeory.ipynb` | Agent memory (checkpointer) |
| `7-create-document.ipynb` | Create documents via agent |

Run notebook cell 0 first — it loads `notebook/setup.py` to bootstrap Django.

## Admin

Documents are registered in Django admin:

```
http://127.0.0.1:8000/admin/
```
