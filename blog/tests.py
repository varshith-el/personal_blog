from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post, Category


# Create your tests here.


class BlogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='test')
        self.post = Post.objects.create(
            title='Test post',
            body='This is a test post.',
        )
        self.post.categories.add(self.category)

    def test_add_post_view(self):
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/add_post.html')

    def test_add_post_form(self):
        response = self.client.post(reverse('add_post'), {
            'title': 'Test post 2',
            'body': 'This is another test post.',
            'categories': self.category.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Test post 2')
