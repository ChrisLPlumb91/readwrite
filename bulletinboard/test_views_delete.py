from django.test import TestCase
from .models import Bulletin, Comment
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


class TestDeleteViews(TestCase):

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

    def test_delete_bulletin_page(self):
        another_bulletin = Bulletin.objects.create(title='Another New Bulletin',
                                                   slug='another-new-bulletin',
                                                   author=self.user_1,
                                                   content='This is a test ' +
                                                   'bulletin.',
                                                   link='https://www.google.ie/',
                                                   status=1,
                                                   edited=False)

        url = reverse('confirm_delete', args=[another_bulletin.slug])
        response = self.client.post(url)

        existing_bulletins = Bulletin.objects.filter(id=another_bulletin.id)

        self.assertEqual(len(existing_bulletins), 0)
        self.assertRedirects(response, '/')

    def test_delete_comment(self):
        another_comment = Comment.objects.create(bulletin=self.bulletin,
                                                 author=self.user_1,
                                                 comment='This is another ' +
                                                 'test comment',
                                                 edited=False)

        url = reverse('comment_delete', args=[self.bulletin.slug])
        query_string = f'?query={another_comment.id}'
        full_url = url + query_string

        response = self.client.post(full_url)

        existing_comments = Comment.objects.filter(id=another_comment.id)

        self.assertEqual(len(existing_comments), 0)
        self.assertRedirects(response, '/post/new-bulletin/')