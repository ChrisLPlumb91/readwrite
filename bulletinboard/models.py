from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, 'Awaiting approval'), (1, 'Approved'))


class Bulletin(models.Model):
    title = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=40, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                               related_name='bulletins')
    content = models.TextField()
    link = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='bulletin_likes')
    edited = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE,
                                 related_name='comments_on_post')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments_by_user')
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_likes')
    edited = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment: "{self.comment}", by {self.author}'

    def number_of_likes(self):
        return self.likes.count()