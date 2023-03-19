from django.test import TestCase
from .forms import BulletinForm, CommentForm


class TestBulletinForm(TestCase):

    def test_title_is_required(self):
        form = BulletinForm({'title': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'This field is required.')

    def test_content_is_required(self):
        form = BulletinForm({'content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'This field is required.')

    def test_link_is_required(self):
        form = BulletinForm({'link': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('link', form.errors.keys())
        self.assertEqual(form.errors['link'][0], 'This field is required.')

    def test_bulletin_meta_class(self):
        form = BulletinForm()
        self.assertEqual(form.Meta.fields, ('title', 'content', 'link'))


class TestCommentForm(TestCase):
    def test_comment_is_required(self):
        form = CommentForm({'comment': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors.keys())
        self.assertEqual(form.errors['comment'][0], 'This field is required.')

    def test_comment_meta_class(self):
        form = CommentForm()
        self.assertEqual(form.Meta.fields, ('comment',))
