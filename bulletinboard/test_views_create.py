from django.test import TestCase
from .models import Bulletin, Comment
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


class TestCreateViews(TestCase):

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

    def test_post_comment_bulletin_page(self):
        url = reverse('bulletin', args=[self.bulletin.slug])
        response = self.client.post(url, {'comment': 'This is a test comment.'})

        new_comment = Comment.objects.get(id=2)

        self.assertEqual(new_comment.comment, 'This is a test comment.')