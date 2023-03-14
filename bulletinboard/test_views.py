from django.test import TestCase
from .models import Bulletin, Comment
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


class TestViews(TestCase):

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

    def test_post_add_bulletin_page(self):
        response = self.client.post('/add',
                                    {
                                        'title': 'Another New Bulletin',
                                        'content': 'This is another test ' +
                                        'bulletin',
                                        'link': 'https://www.youtube.com/',
                                    })

        new_bulletin = Bulletin.objects.get(slug='another-new-bulletin')

        self.assertEqual(new_bulletin.author, self.user_1)
        self.assertEqual(new_bulletin.status, 0)
        self.assertRedirects(response, '/')

    def test_get_edit_bulletin_page(self):
        url = reverse('edit', args=[self.bulletin.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_bulletin.html')

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

        existing_items = Bulletin.objects.filter(id=another_bulletin.id)

        self.assertEqual(len(existing_items), 0)
        self.assertRedirects(response, '/')

    def test_post_comment_bulletin_page(self):
        url = reverse('bulletin', args=[self.bulletin.slug])
        response = self.client.post(url, {'comment': 'This is a test comment.'})

        new_comment = Comment.objects.get(id=2)

        self.assertEqual(new_comment.comment, 'This is a test comment.')

    def test_get_edit_comment_bulletin_page(self):
        url = reverse('comment_edit', args=[self.bulletin.slug])

        query_string_1 = f'?query={self.comment.id}'
        full_url_1 = url + query_string_1

        response_1 = self.client.get(full_url_1)
        self.assertEqual(response_1.status_code, 200)

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

        existing_items = Comment.objects.filter(id=another_comment.id)

        self.assertEqual(len(existing_items), 0)
        self.assertRedirects(response, '/post/new-bulletin/')