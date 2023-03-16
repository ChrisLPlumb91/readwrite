from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, 'Awaiting approval'), (1, 'Approved'))


class Bulletin(models.Model):
    """
    This is the model for Bulletins, which are posts made to the site.

    The slug field is populated with a slug version of the title,
    which is used in almost all the site's url patterns.

    The author field uses Django's build in User model,
    and this field is set to cascade if deleted. In other words,
    if a user is deleted, so too are all the bulletins
    that they posted.

    The created_on field uses auto_now_add to capture
    the time and date at which a bulletin object is created,
    whereas the updated_on uses auto_now to enable this
    same timestamp to be changed every time the object
    is saved, i.e. changed. The value for the created_on
    field is displayed in the template for every bulletin,
    while the updated_on field is only displayed if the
    bulletin is edited, which is determined by the value
    of the edited field.

    The status field is used to approve bulletins from
    the admin panel. Each view that queries the Bulletin
    table only requests bulletins with a status value of 1,
    i.e. approved bulletins. This ensures that only approved
    bulletins are displayed in templates.

    The likes field is linked to the User table as well,
    and is used to track which users have liked a bulletin.
    As this is a many-to-many field, users must be added
    to an intermediate likes table using the add and remove
    methods in views.

    The meta class orders the records in the Bulletin table
    by the date they were created, i.e. in descending order,
    from newest to oldest.

    The __str__ method simply returns the title of the bulletin.

    The number_of_likes method counts the number of records
    in the likes bridge table for a given bulletin,
    thereby returning the number of likes that bulletin
    has received. This information is used in templates.
    """
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
    """
    This is the model for Comments, which are left on bulletins by users
    of the site.

    This model is similar to the Bulletin model, but one key difference
    is that it has a foreign key field that links it to the Bulletin
    table. This is necessary because comments are left on specific
    bulletins. The use of cascade here means that if a bulletin is
    deleted, then all the comments related to it will be deleted
    as well.

    The author field uses the User table, just as the same field
    in the Bulletin model does, and again, because of the use of
    cascade, if a user is deleted, so too are all of their comments.

    The "comment" text field contains the comment itself.

    The created_on, likes, edited, and updated_on fields all
    functionally identically to the same fields in the Bulletin
    model (see above).

    This model does not have a status field, as comments do not
    have to be approved.

    As with the bulletin model, comments are ordered within their
    table from newest to oldest.

    The __str__ method for this model returns a formatted string
    that includes the comment itself, as well as the name of the user
    who posted it.
    """
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
