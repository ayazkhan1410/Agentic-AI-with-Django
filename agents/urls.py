from django.urls import path
from agents.views import (
    RetrieveDocumentDataView, RetrieveSingleDocumentDataView
)


urlpatterns = [
    path("retrieve-document/", RetrieveDocumentDataView.as_view()),
    path("retrieve-single-document/<int:pk>/", RetrieveSingleDocumentDataView.as_view()),
]
