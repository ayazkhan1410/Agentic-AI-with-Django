from django.urls import path
from agents.views import (
    RetrieveDocumentDataView, RetrieveSingleDocumentDataView,
    ChatView
)


urlpatterns = [
    path("retrieve-document/", RetrieveDocumentDataView.as_view()),
    path(
        "retrieve-single-document/<int:pk>/",
        RetrieveSingleDocumentDataView.as_view()
    ),
    path("chat/", ChatView.as_view()),
]
