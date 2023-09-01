from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Content
from content import serializers


class ContentViewSet(viewsets.ModelViewSet):
    """View for managing content apis"""
    serializer_class = serializers.ContentDetailSerializer
    queryset = Content.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieving contents for auth users"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Returns """
        if self.action == 'list':
            return serializers.ContentSerializer
        
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
