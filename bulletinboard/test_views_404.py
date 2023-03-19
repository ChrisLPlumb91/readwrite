from django.test import TestCase
from .models import Bulletin, Comment
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


class Test404Views(TestCase):

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

    def test_404_when_add_not_logged_in(self):
        self.client.logout()

        response = self.client.get('/add')
        self.assertEqual(response.status_code, 404)

        self.client.login(username=self.user_1.username,
                          password='test')

    def test_404_when_try_edit_other_bulletin(self):
        self.client.logout()
        user_2 = User.objects.create_user(username='test_user_2',
                                          password='test')

        self.client.login(username=user_2.username,
                          password='test')

        url = reverse('edit', args=[self.bulletin.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

        self.client.logout()
        user_2.delete()
        self.client.login(username=self.user_1.username,
                          password='test')

    def test_404_when_try_delete_other_bulletin(self):
        self.client.logout()
        user_2 = User.objects.create_user(username='test_user_2',
                                          password='test')

        self.client.login(username=user_2.username,
                          password='test')

        url = reverse('confirm_delete', args=[self.bulletin.slug])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

        existing_bulletins = Bulletin.objects.filter(id=self.bulletin.id)

        self.assertEqual(len(existing_bulletins), 1)

        self.client.logout()
        user_2.delete()
        self.client.login(username=self.user_1.username,
                          password='test')

    def test_404_when_try_edit_other_comment(self):
        self.client.logout()

        user_2 = User.objects.create_user(username='test_user_2',
                                          password='test')

        self.client.login(username=user_2.username,
                          password='test')

        url = reverse('comment_edit', args=[self.bulletin.slug])

        query_string = f'?query={self.comment.id}'
        full_url = url + query_string

        response = self.client.get(full_url)
        self.assertEqual(response.status_code, 404)

        self.client.logout()
        user_2.delete()
        self.client.login(username=self.user_1.username,
                          password='test')

    def test_404_when_try_delete_other_comment(self):
        self.client.logout()

        user_2 = User.objects.create_user(username='test_user_2',
                                          password='test')

        self.client.login(username=user_2.username,
                          password='test')

        url = reverse('comment_delete', args=[self.bulletin.slug])
        query_string = f'?query={self.comment.id}'
        full_url = url + query_string

        response = self.client.post(full_url)
        self.assertEqual(response.status_code, 404)

        existing_comments = Comment.objects.filter(id=self.comment.id)

        self.assertEqual(len(existing_comments), 1)

        self.client.logout()
        user_2.delete()
        self.client.login(username=self.user_1.username,
                          password='test')

    def test_404_when_try_access_like_bulletin_url(self):
        self.client.logout()

        home_url = reverse('home')
        bulletin_url = reverse('bulletin', args=[self.bulletin.slug])
        like_url = reverse('bulletin_like', args=[self.bulletin.slug])

        full_url_1 = like_url + f'?query={home_url}'
        full_url_2 = like_url + f'?query={bulletin_url}'

        response_1 = self.client.post(full_url_1)
        self.assertTrue(response_1.status_code, 404)
        self.assertEqual(self.bulletin.number_of_likes(), 0)

        response_2 = self.client.post(full_url_2)
        self.assertTrue(response_2.status_code, 404)
        self.assertEqual(self.bulletin.number_of_likes(), 0)

        self.client.login(username=self.user_1.username,
                          password='test')

    def test_404_when_try_access_like_comment_url(self):
        self.client.logout()

        bulletin_url = reverse('bulletin', args=[self.bulletin.slug])
        comment_like_url = reverse('comment_like', args=[self.bulletin.slug])

        full_url = comment_like_url + f'?query={self.comment.id}'

        response = self.client.post(full_url)
        self.assertTrue(response.status_code, 404)
        self.assertEqual(self.comment.number_of_likes(), 0)

        self.client.login(username=self.user_1.username,
                          password='test')
