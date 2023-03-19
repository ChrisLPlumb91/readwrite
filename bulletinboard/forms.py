from django import forms
from .models import Bulletin, Comment


class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ('title', 'content', 'link')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
