from django.test import TestCase
from .models import Bulletin, Comment
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


class TestReadViews(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_1 = User.objects.create_user(username='test_user',
                                              password='test')

    @classmethod
    def tearDownClass(cls):
        cls.user_1.delete()

    def setUp(self):
        self.bulletin_title = 'New Bulletin'
        self.title_slug = slugify(self.bulletin_title)
        self.bulletin_title_edited = 'Edited Bulletin'

        self.client.login(username=self.user_1.username,
                          password='test')

        self.bulletin = Bulletin.objects.create(title=self.bulletin_title,
                                                slug=self.title_slug,
                                                author=self.user_1,
                                                content='This is a test ' +
                                                'bulletin.',
                                                link='https://www.google.ie/',
                                                status=1,
                                                edited=False)

        self.comment = Comment.objects.create(bulletin=self.bulletin,
                                              author=self.user_1,
                                              comment='This is a test comment',
                                              edited=False)

    def tearDown(self):
        self.client.logout()
        self.bulletin.delete()
        self.comment.delete()

    def test_get_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_bulletin_detail_page(self):
        url = reverse('bulletin', args=[self.bulletin.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_add_bulletin_page(self):
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_bulletin.html')

    def test_get_edit_bulletin_page(self):
        url = reverse('edit', args=[self.bulletin.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_bulletin.html')

    def test_get_edit_comment_bulletin_page(self):
        url = reverse('comment_edit', args=[self.bulletin.slug])

        query_string_1 = f'?query={self.comment.id}'
        full_url_1 = url + query_string_1

        response_1 = self.client.get(full_url_1)
