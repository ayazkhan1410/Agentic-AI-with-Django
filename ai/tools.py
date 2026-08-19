from django.db.models import Q

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from agents.models import Document

from tmbd.client import search_movie, get_movie_details


# =============================
# Document Tools
# =============================
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


def get_documents(
    config: RunnableConfig,
    limit: int = 5,
    maximum_limit: int = 25,
):
    """Get Last 5 documents and return them in a list."""
    user_id = config.get("configurable", {}).get("user_id")
    print("USER ID IN GET DOCUMENTS:", user_id)

    limit = max(1, min(limit, maximum_limit))

    try:
        documents = Document.objects.select_related(
            "owner"
        ).filter(
            active=True,
            owner__id=user_id
        ).order_by("-created_at")[:limit]
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


def search_documents(
    query: str,
    config: RunnableConfig = None,
    limit: int = 5,
    maximum_limit: int = 25,
) -> dict:
    """Search for documents by title or content."""
    user_id = config.get("configurable", {}).get("user_id")

    limit = max(1, min(limit, maximum_limit))

    try:
        default_lookups = {
            "active": True,
            "owner__id": user_id,
        }
        documents = Document.objects.filter(**default_lookups).filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )[:limit]
    except Exception as e:
        return {"error": f"Error searching documents: {e}"}

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


def delete_document(
    document_id: int,
    config: RunnableConfig = None
) -> dict:
    """Delete a document by ID."""
    user_id = config.get("configurable", {}).get("user_id")
    try:
        document = Document.objects.filter(
            id=document_id, owner__id=user_id
        ).first()
        if not document:
            return {"error": f"Document with id {document_id} not found."}
        document.delete()
    except Exception as e:
        return {"error": f"Error deleting document: {e}"}
    return {"success": f"Document with id {document_id} deleted successfully."}


# =============================
# Movie Discovery Tools
# =============================
def search_movie_tool(
    query: str,
    config: RunnableConfig,
    limit: int = 5,
    maximum_limit: int = 25,
):
    """
    Search for movies by title or content using the provided query.

    Args:
        query (str): The search term to find movies by title or content.
        config (RunnableConfig): Configuration that should include user
            context.
        limit (int, optional): The maximum number of movie results to
            return. Defaults to 5.
        maximum_limit (int, optional): The upper bound for result
            limitation. Defaults to 25.
    Returns:
        list: A list of movie objects containing details
           matched by the search query.
    """

    user_id = config.get("configurable", {}).get("user_id")
    print("USER ID IN GET DOCUMENTS:", user_id)

    limit = max(1, min(limit, maximum_limit))

    # Search for a movie
    response = search_movie(query).get("results", [])[:limit]
    print('Search Movie Response: ', response)
    return response


def get_movie_details_tool(movie_id: int, config: RunnableConfig):
    """
    Retrieve details for a specific movie by its movie ID.

    Args:
        movie_id (int): The unique identifier of the movie.
        config (RunnableConfig): Configuration that should include user
            context.
    Returns:
        dict: A dictionary containing detailed information about the movie.
    """
    user_id = config.get("configurable", {}).get("user_id")
    print("USER ID IN GET MOVIE DETAILS:", user_id)

    # Get movie details
    movie_details = get_movie_details(movie_id)
    print('Movie Details: ', movie_details)
    return movie_details


# =============================
# Document Tools
# =============================
get_document_tool = tool(get_document)
get_documents_tool = tool(get_documents)
create_document_tool = tool(create_document)
update_document_tool = tool(update_document)
search_documents_tool = tool(search_documents)
delete_document_tool = tool(delete_document)


# =============================
# Movie Discovery Tools
# =============================
search_movie_tool = tool(search_movie_tool)
get_movie_details_tool = tool(get_movie_details_tool)
