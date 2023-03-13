from django.test import TestCase
from .models import Bulletin, Comment
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_1 = User.objects.create_user(username='test_user',
                                              password='test')

    @classmethod
    def tearDownClass(cls):
        cls.user_1.delete()

    def test_get_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_add_bulletin_page(self):
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_bulletin.html')

    def test_get_edit_bulletin_page(self):
        bulletin_title = 'New Bulletin'
        title_slug = slugify(bulletin_title)

        self.client.login(username=self.user_1.username,
                          password=self.user_1.password)

        bulletin = Bulletin.objects.create(title=bulletin_title,
                                           slug=title_slug,
                                           author=self.user_1,
                                           content='This is a test bulletin.',
                                           link='https://www.google.ie/',
                                           edited=False)
        bulletin.likes.add(self.user_1)

        response = self.client.get(f'/edit/{bulletin.slug}')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_bulletin.html')