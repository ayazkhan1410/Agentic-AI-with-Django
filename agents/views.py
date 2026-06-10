import traceback

from agents.models import Document
from agents.serializers import DocumentSerializer

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
            document = Document.objects.get(id=pk)
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
