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

    def tearDown(self):
        self.client.logout()
        self.bulletin.delete()

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

        self.assertEqual(updated_bulletin.slug, 'edited-bulletin')
        self.assertRedirects(response, response.url)

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
        response = self.client.post(url, {'comment': 'This is a new comment.'})

        new_comment = Comment.objects.get(id=1)

        self.assertEqual(new_comment.comment, 'This is a new comment.')