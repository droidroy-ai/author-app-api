from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Content

from content.serializers import (
    ContentSerializer,
    ContentDetailSerializer,
)


CONTENTS_URL = reverse('content:content-list')


def detail_url(content_id):
    return reverse('content:content-detail', args=[content_id])


def create_content(user, **params):
    """Create and return a test content obj"""
    defaults = {
        'title': 'Sample Content title',
        'body': 'Sample body',
        'summary': 'Sample summary',
    }
    defaults.update(params)

    content = Content.objects.create(user=user, **defaults)
    return content


class PublicContentAPITests(TestCase):
    """Test unauthenticated api requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(CONTENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateContentAPITests(TestCase):
    """Test authenticated api requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_contents(self):
        """Test retrieving list of contents"""
        create_content(user=self.user)
        create_content(user=self.user)

        res = self.client.get(CONTENTS_URL)

        contents = Content.objects.all().order_by('-id')
        serializer = ContentSerializer(contents, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_content_list_lim_to_user(self):
        """Test list of contents is limited to auth users"""
        new_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
        )
        create_content(user=new_user)
        create_content(user=self.user)

        res = self.client.get(CONTENTS_URL)
        contents = Content.objects.filter(user=self.user)
        serializer = ContentSerializer(contents, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_get_content_detail(self):
    #     """Test get content detail"""
    #     content = create_content(user=self.user)

    #     url = detail_url(content.id)
    #     res = self.client.get(url)

    #     serializer = ContentDetailSerializer(res)
    #     self.assertEqual(res.data, serializer.data)

    def test_create_content(self):
        payload = {
            'title': 'Sample Content',
            'body': 'Sample body',
            'summary': 'Sample summary',
        }
        res = self.client.post(CONTENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        content = Content.objects.get(id=res.data['id'])
        for k,v in payload.items():
            self.assertEqual(getattr(content, k), v)
        self.assertEqual(content.user, self.user)
