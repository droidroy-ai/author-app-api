from rest_framework import serializers

from core.models import Content


class ContentSerializer(serializers.ModelSerializer):
    """Serializer for content objects"""

    class Meta:
        model = Content
        fields = [
            'id',
            'title',
            'summary',
        ]
        read_only_fields = ['id']


class ContentDetailSerializer(serializers.ModelSerializer):
    """Serializer for content detail"""

    class Meta:
        model = Content
        fields = [
            'id',
            'title',
            'body',
            'summary',
        ]
        read_only_fields = ['id']
