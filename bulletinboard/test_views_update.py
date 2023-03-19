from django.test import TestCase
from .models import Bulletin, Comment
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


class TestUpdateViews(TestCase):

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

    def test_post_edit_bulletin_page_home_redirect(self):
        url_1 = reverse('home')
        url_2 = reverse('edit', args=[self.bulletin.slug])

        edit_from_home_url = url_2 + '?query=' + url_1

        response = self.client.post(edit_from_home_url,
                                    {
                                        'title': self.bulletin_title_edited,
                                        'content': 'bulletin edited',
                                        'link': 'https://github.com/'
                                    })

        updated_bulletin = Bulletin.objects.get(id=self.bulletin.id)

        self.assertEqual(updated_bulletin.slug, 'edited-bulletin')
        self.assertRedirects(response, '/')

    def test_post_edit_bulletin_page_post_redirect(self):
        url_1 = reverse('bulletin', args=[self.bulletin.slug])
        url_2 = reverse('edit', args=[self.bulletin.slug])

        edit_from_post_url = url_2 + '?query=' + url_1

        response = self.client.post(edit_from_post_url,
                                    {
                                        'title': self.bulletin_title_edited,
                                        'content': 'bulletin edited',
                                        'link': 'https://github.com/'
                                    })

        updated_bulletin = Bulletin.objects.get(id=self.bulletin.id)

        self.assertTrue(updated_bulletin.edited)
        self.assertRedirects(response, f'/post/{updated_bulletin.slug}/')

    def test_post_edit_comment_bulletin_page(self):
        url = reverse('comment_edit', args=[self.bulletin.slug])

        query_string_1 = f'?query={self.comment.id}'
        full_url_1 = url + query_string_1

        query_string_2 = f'?query={full_url_1}'
        full_url_2 = url + query_string_2

        self.assertEqual(full_url_2,
                         '/edit_comment/new-bulletin?query=/' +
                         'edit_comment/new-bulletin?query=1')

        response_2 = self.client.post(full_url_2,
                                      {'comment': 'This comment has ' +
                                       'been changed'})

        updated_comment = Comment.objects.get(id=1)

        self.assertTrue(updated_comment.edited)
        self.assertRedirects(response_2, '/post/new-bulletin/')

    def test_post_like_bulletin_home_page(self):
        home_url = reverse('home')
        like_url = reverse('bulletin_like', args=[self.bulletin.slug])

        full_url = like_url + f'?query={home_url}'

        response_1 = self.client.post(full_url)
        self.assertTrue(self.bulletin.likes.filter(id=self.user_1.id).exists())
        self.assertRedirects(response_1, home_url)

        response_2 = self.client.post(full_url)
        (self.assertFalse(self.bulletin.likes.filter(id=self.user_1.id)
                          .exists()))
        self.assertRedirects(response_2, home_url)

    def test_post_like_bulletin_bulletin_page(self):
        bulletin_url = reverse('bulletin', args=[self.bulletin.slug])
        like_url = reverse('bulletin_like', args=[self.bulletin.slug])

        full_url = like_url + f'?query={bulletin_url}'

        response_1 = self.client.post(full_url)
        self.assertTrue(self.bulletin.likes.filter(id=self.user_1.id).exists())
        self.assertRedirects(response_1, bulletin_url)

        response_2 = self.client.post(full_url)
        (self.assertFalse(self.bulletin.likes.filter(id=self.user_1.id)
                          .exists()))
        self.assertRedirects(response_2, bulletin_url)

    def test_post_like_comment_bulletin_page(self):
        bulletin_url = reverse('bulletin', args=[self.bulletin.slug])
        comment_like_url = reverse('comment_like', args=[self.bulletin.slug])

        full_url = comment_like_url + f'?query={self.comment.id}'

        response_1 = self.client.post(full_url)
        self.assertTrue(self.comment.likes.filter(id=self.user_1.id).exists())
        self.assertRedirects(response_1, bulletin_url)

        response_2 = self.client.post(full_url)
        self.assertFalse(self.comment.likes.filter(id=self.user_1.id).exists())
        self.assertRedirects(response_2, bulletin_url)
