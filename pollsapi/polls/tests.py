from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory


from .views import PollViewSet

class TestPoll(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PollViewSet.as_view({'get': 'list'})
        self.url = '/pools/'

    def test_list(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(
            response.status_code, 200, 'ddd'
        )
