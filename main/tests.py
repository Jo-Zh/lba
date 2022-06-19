import unittest
from django.test import Client
from django.test import TestCase
from .models import Posts, User, Comments, Notes, Category
# Create your tests here.

#Test models
class PostsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='avatar')
        Posts.objects.create(title='testPost', creater=User.objects.get(username='avatar'))
    
    def test_description(self):
        post=Posts.objects.get(title='testPost')
        field_label=post._meta.get_field('cover').verbose_name
        self.assertEqual(field_label, 'cover')


# test GET POST responses on URL

# HomePage
class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/home')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 2 posts.
        self.assertEqual(len(response.context['posts']), 0)