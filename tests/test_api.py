from tests.base import APITestCase
from fastapi import status


class TestJokeApi(APITestCase):
    base = '/jokes'

    def test_get_random(self):
        response = self.client.get(self.base)
        self.assertSuccess(response, status.HTTP_200_OK)

        content = response.json()
        self.assertIsInstance(content['joke'], str)
        self.assertTrue(content['joke'])

    def test_with_mock(self):
        self.mock_request.get('')
