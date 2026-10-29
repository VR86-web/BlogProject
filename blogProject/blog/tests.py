from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post


class PostSearchTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username='search-author',
            password='test-password',
        )
        self.post = Post.objects.create(
            author=self.author,
            title='A quiet morning',
            slug='quiet-morning',
            body='A rare phrase about quantum gardening appears here.',
            status=Post.Status.PUBLISHED,
        )

    def test_search_finds_published_posts_by_body_text(self):
        response = self.client.get(
            reverse('blog:post_search'),
            {'query': 'quantum gardening'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post, response.context['results'])

    def test_search_still_finds_posts_by_fuzzy_title(self):
        response = self.client.get(
            reverse('blog:post_search'),
            {'query': 'quiet mornin'},
        )

        self.assertIn(self.post, response.context['results'])
