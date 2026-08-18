import requests
from aiengine import settings


def get_headers():
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.MOVIE_DB_READ_ACCESS_TOKEN}",
    }


def search_movie(query):
    params = {
        "query": query,
        "include_adult": "false",
        "language": "en-US",
        "page": 1,
    }

    try:
        response = requests.get(
            settings.SEARCH_MOVIE_URL,
            headers=get_headers(),
            params=params,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Error searching movie: {e}"
        ) from e


def get_movie_details(movie_id: int):
    try:
        url = f"{settings.MOVIE_DETAILS_URL.format(movie_id=movie_id)}"
        response = requests.get(url, headers=get_headers(), timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Error getting movie details: {e}"
        ) from e
