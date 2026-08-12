import traceback
import uuid

from django.contrib.auth.models import User

from agents.models import Document
from agents.serializers import ChatSerializer, DocumentSerializer
from ai.agents import get_document_agent

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RetrieveDocumentDataView(APIView):
    def get(self, request):
        try:
            document_queryset = Document.objects.all()
            serializer = DocumentSerializer(document_queryset, many=True)
            return Response({
                "message": "Documents retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetrieveSingleDocumentDataView(APIView):
    def get(self, request, pk):
        try:
            document = Document.objects.get(
                id=pk,
                active=True
            )
            serializer = DocumentSerializer(document)
            return Response({
                "message": "Document retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatView(APIView):
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(
            is_superuser=True
        ).first()
        if not user:
            return Response({
                "error": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        message = serializer.validated_data["message"]

        try:
            agent = get_document_agent()
            result = agent.invoke(
                {
                    "messages": [
                        {"role": "user", "content": message},
                    ],
                },
                {
                    "configurable": {
                        "user_id": user.id,
                        "thread_id": str(uuid.uuid4()),
                    },
                },
            )

            reply = result["messages"][-1].content.strip().replace('\n', '')
            return Response({
                "message": "Chat response generated successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                },
                "agent_reply": reply,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
