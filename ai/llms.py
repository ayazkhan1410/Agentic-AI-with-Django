from django.conf import settings
from langchain_openai import ChatOpenAI


def get_open_ai_models(model="gpt-5.4-mini"):
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=0.0,
        max_retries=2,
        api_key=settings.OPENAI_API_KEY,
    )
