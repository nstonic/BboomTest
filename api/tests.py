from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class UserTestCase(APITestCase):

    def test_registration(self):
        user = CustomUser.objects.create_user(
            username='User',
            email='user@user.com',
            password='MegaPass123'
        )
        user_data = {
            'user': user.username,
            'email': user.email,
            'password': 'MegaPass123'
        }
        response = self.client.post('/api-auth/login', user_data)
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

        response = self.client.get('/api/users/')
        self.assertEqual(response.json()[0]['username'], user.username)
        self.assertEqual(response.json()[0]['email'], user.email)


class PostCreationTestCase(APITestCase):

    def test_registration(self):
        user = CustomUser.objects.create_user(
            username='User',
            email='user@user.com',
            password='MegaPass123'
        )
        data = {
            'title': 'post1',
            'body': 'post body',
            'user': user.id
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/api/users/1/posts/')
        self.assertEqual(response.json()[0]['title'], data['title'])
        self.assertEqual(response.json()[0]['body'], data['body'])
        self.assertEqual(response.json()[0]['user'], data['user'])
        post_id = response.json()[0]['id']

        response = self.client.delete(f'/api/posts/{post_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
