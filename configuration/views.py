from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheck(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response("ok", status=status.HTTP_200_OK)
