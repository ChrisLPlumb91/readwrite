from django.test import TestCase
from .models import Bulletin, Comment
from django.contrib.auth.models import User


class TestModels(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test_user',
                                            password='test')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.bulletin = Bulletin.objects.create(title='New Bulletin',
                                                author=self.user,
                                                content='This is a ' +
                                                'test bulletin.',
                                                link='https://www.google.ie/')

        self.comment = Comment.objects.create(bulletin=self.bulletin,
                                              author=self.user,
                                              comment='This is ' +
                                              'a test comment.')

    def tearDown(self):
        self.bulletin.delete()
        self.comment.delete()

    def test_new_bulletin_defaults(self):
        self.assertEqual(self.bulletin.status, 0)
        self.assertFalse(self.bulletin.edited)

    def test_bulletin_str_method(self):
        self.assertEqual(self.bulletin.__str__(), self.bulletin.title)

    def test_bulletin_likes_method(self):
        self.bulletin.likes.add(self.user)
        self.assertEqual(self.bulletin.number_of_likes(), 1)
        self.bulletin.likes.remove(self.user)
        self.assertEqual(self.bulletin.number_of_likes(), 0)

    def test_new_comment_default(self):
        self.assertFalse(self.comment.edited)

    def test_comment_str_method(self):
        self.assertEqual(self.comment.__str__(), 'Comment: ' +
                         '"This is a test comment.", by test_user')

    def test_comment_likes_method(self):
        self.comment.likes.add(self.user)
        self.assertEqual(self.comment.number_of_likes(), 1)
        self.comment.likes.remove(self.user)
        self.assertEqual(self.comment.number_of_likes(), 0)
