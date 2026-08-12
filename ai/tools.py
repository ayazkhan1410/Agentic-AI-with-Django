from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from agents.models import Document


def get_document(document_id, config: RunnableConfig):
    """Get one document by ID."""
    user_id = config.get("configurable", {}).get("user_id")

    try:
        document = (
            Document.objects.select_related("owner")
            .filter(id=document_id, active=True, owner__id=user_id)
            .first()
        )
        if not document:
            return {"error": f"Document with id {document_id} not found."}
    except Exception as e:
        return {"error": f"Error getting document: {e}"}

    owner = document.owner
    return {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "active": document.active,
        "owner": owner.username if owner else None,
        "created_at": document.created_at.strftime("%Y-%m-%d %I:%M:%S %p"),
        "updated_at": document.updated_at.strftime("%Y-%m-%d %I:%M:%S %p"),
    }


def get_documents(config: RunnableConfig):
    """Get Last 5 documents and return them in a list."""
    user_id = config.get("configurable", {}).get("user_id")
    print("USER ID IN GET DOCUMENTS:", user_id)

    try:
        documents = Document.objects.select_related(
            "owner"
        ).filter(
            active=True,
            owner__id=user_id
        ).order_by("-created_at")[:5]
    except Document.DoesNotExist:
        return {"error": "No documents found."}
    except Exception as e:
        return {"error": f"Error getting documents: {e}"}

    response_data = []
    for document in documents:
        owner = document.owner
        response_data.append({
            "id": document.id,
            "title": document.title,
            "content": document.content,
            "active": document.active,
            "owner": owner.username if owner else None,
            "created_at": document.created_at.strftime("%Y-%m-%d %I:%M:%S %p"),
            "updated_at": document.updated_at.strftime("%Y-%m-%d %I:%M:%S %p"),
        })

    return response_data


def create_document(
    title: str,
    content: str,
    config: RunnableConfig
) -> dict:
    """Create a new document."""
    user_id = config.get("configurable", {}).get("user_id")

    try:
        document = Document.objects.create(
            title=title,
            content=content,
            owner_id=user_id
        )
    except Exception as e:
        return {"error": f"Error creating document: {e}"}

    return {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "active": document.active,
        "owner": document.owner.username if document.owner else None,
        "created_at": document.created_at.strftime("%Y-%m-%d %I:%M:%S %p"),
        "updated_at": document.updated_at.strftime("%Y-%m-%d %I:%M:%S %p"),
    }


def update_document(
    document_id: int,
    title: str | None = None,
    content: str | None = None,
    config: RunnableConfig = None
) -> dict:
    """Update an existing document."""
    user_id = config.get("configurable", {}).get("user_id")

    try:
        document = Document.objects.filter(
            id=document_id,
            owner__id=user_id
        ).first()
        if not document:
            return {"error": f"Document with id {document_id} not found."}

        if title is not None:
            document.title = title
        if content is not None:
            document.content = content
        if title is None and content is None:
            return {"error": "No fields to update."}

        document.save()
    except Exception as e:
        return {"error": f"Error updating document: {e}"}

    return {
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "active": document.active,
        "owner": document.owner.username if document.owner else None,
        "created_at": document.created_at.strftime("%Y-%m-%d %I:%M:%S %p"),
        "updated_at": document.updated_at.strftime("%Y-%m-%d %I:%M:%S %p"),
    }


get_document_tool = tool(get_document)
get_documents_tool = tool(get_documents)
create_document_tool = tool(create_document)
update_document_tool = tool(update_document)
