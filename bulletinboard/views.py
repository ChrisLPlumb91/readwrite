from django.db.models import F, Max
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from .models import Bulletin, Comment
from .forms import BulletinForm, CommentForm
from django.template.defaultfilters import slugify
from django.contrib import messages


class BulletinList(generic.ListView):
    """
    This is the view that displays the main landing page.
    ListView is extended here as the main page is simply
    a list of any bulletins that have been approved.
    This view also ensures that a maximum of 10 bulletins
    are shown on the main page at a time, and that they
    are ordered in such a way that the most recently posted
    one appears at the top.

    """
    model = Bulletin
    queryset = Bulletin.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 10


class BulletinDetail(View):
    """
    This view displays an individual bulletins page,
    and also handles any post requests made by the comment
    form on said page.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        This is the get method for an individual bulletins page.
        It queries both the Bulletin and Comment tables so that
        it can display the bulletin whose link you have followed,
        as well as any comments that have been made on it.
        It also passes a blank comment form to the template
        for the page so that users can submit their comments
        through it.

        The arcane-looking line that gets the bulletins comments
        is necessary to avoid duplication of comments when "liking"
        them. Initially, I was using order_by('likes'), but it was
        causing the above error. This seems to have to do with the
        fact that likes is a many-to-many field, and that order_by
        uses JOIN queries.
        """
        queryset = Bulletin.objects.filter(status=1)
        specific_bulletin = get_object_or_404(queryset, slug=slug)

        comments = (Comment.objects.filter(bulletin=specific_bulletin)
                    .annotate(likes_temp=Max('likes'))
                    .order_by(F('likes_temp')
                    .desc(nulls_last=True)))

        return render(
            request,
            'bulletin.html',
            {
                'bulletin': specific_bulletin,
                'comments': comments,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        This is the post method for a specific bulletins page.
        It gets the data from the submitted comment form
        and then creates a comment from it, before inserting
        it in the Comment table.

        Once the view has done this, it displays the bulletin
        page again, and because the new comment has been added
        to the Comment table, it now displays among the other
        comments.
        """
        if request.user.is_authenticated:
            queryset = Bulletin.objects.filter(status=1)
            specific_bulletin = get_object_or_404(queryset, slug=slug)

            comments = (Comment.objects.filter(bulletin=specific_bulletin)
                        .annotate(likes_temp=Max('likes'))
                        .order_by(F('likes_temp')
                        .desc(nulls_last=True)))

            comment_form = CommentForm(data=request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.bulletin = specific_bulletin
                comment.author = request.user
                comment.save()
                messages.success(request, 'You left a comment on ' +
                                 'this bulletin.')
            else:
                comment_form = CommentForm()

            return render(
                request,
                'bulletin.html',
                {
                    'bulletin': specific_bulletin,
                    'comments': comments,
                    'comment_form': CommentForm()
                },
            )
        else:
            raise Http404


class AddBulletin(View):
    """
    This view displays the page for adding a new bulletin,
    and also handles post requests from said pages form.
    """
    def get(self, request):
        """
        This is the get method for the add bulletin page.
        As the user should only be able to add a bulletin
        if they are logged in, a check is performed to
        see if they are before rendering the page.
        The link / button doesn't actually work
        if the user isn't logged in, but that doesn't
        stop them from typing the add page's url into
        their browser and circumventing this, hence
        the if statement in this method. If they aren't
        logged in, attempting to navigate to the add
        URL will raise a 404.

        Otherwise, a form is instantiated and passed
        to the page.
        """
        if request.user.is_authenticated:
            return render(
                request,
                'add_bulletin.html',
                {
                    'bulletin_form': BulletinForm()
                },
            )
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        """
        This is the post method for the add bulletin page.
        It receives forms submitted on said page.

        Before, it was possible for the form to fail to submit
        even though all its fields were completed. This is because
        the title and slug fields of the Bulletin model have
        their unique parameters set to True. The else clause
        informs the user that this has happened. Without it,
        no such information is given.

        Messages are used to convey the above information,
        and they are also used to inform the user that an admin
        must review their submission, if it is successful.
        """
        if request.user.is_authenticated:
            bulletin_form = BulletinForm(data=request.POST)

            if bulletin_form.is_valid():
                post = bulletin_form.save(commit=False)
                post.slug = slugify(post.title)
                post.author = request.user
                post.save()

                messages.info(request, 'Your post will appear below ' +
                              'if and when it is approved by a moderator')

                return redirect('home')
            else:
                messages.error(request, 'This title has already been used. ' +
                               'Please choose another.')
                return render(
                    request,
                    'add_bulletin.html',
                    {
                        'bulletin_form': bulletin_form
                    },
                )
        else:
            raise Http404


class EditBulletin(View):
    """
    This is the view for the edit bulletin page. It displays it
    for each bulletin, and also handles post requests from its
    form.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        This is the get method for the edit bulletin page.
        It instantiates a form for submitting bulletin data,
        populates it with the data from the bulletin you have
        selected, and then displays the form pre-populated
        with said data, showing the user the current state
        of the bulletin.

        At the template level, the edit button is only available
        on bulletins posted by the user who posted them,
        and they also must be logged in.

        To prevent non-registered users from accessing
        edit pages, I used the get_object_or_404 method
        and passed the current user as the value for
        the author field of the Bulletin table.
        Anonymous users cannot make bulletins,
        so a bulletin will not be found, and the 404
        page will be displayed.
        """
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug, author=request.user)

        bulletin_form = BulletinForm(instance=bulletin)

        return render(
            request,
            'edit_bulletin.html',
            {
                'bulletin_form': bulletin_form,
                'bulletin': bulletin,
                'original_url_query': request.GET.get('query'),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        This is the post method for the edit bulletin page.
        It instantiates a bulletin form and populates it with
        whatever was in the form on the page when the user
        clicked submit.

        From here, it first checks to see if any changes were made
        to the bulletin by comparing the bulletin's yet-to-be-changed
        fields to the submitted data. If the two are the same,
        a message is displayed informing the user of this, and
        the page is reloaded.

        If any of the data is new, the form information is used to
        update the bulletin.

        Because the edit page can be accessed from either the main
        page or an individual bulletins page, there are several if
        statements that check the urls passed via query string
        to see which page the user has come from. The user is
        redirected accordingly.

        Finally, the else at the bottom alerts the user if they
        have changed the bulletins title to one that has already
        been taken (see the add bulletin view above).
        """
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug, author=request.user)

        bulletin_form = BulletinForm(data=request.POST, instance=bulletin)

        if (bulletin.title == bulletin_form.data['title'] and
                bulletin.content == bulletin_form.data['content'] and
                bulletin.link == bulletin_form.data['link']):

            messages.warning(request, "You didn't make any changes " +
                             "to your bulletin...")

            return HttpResponseRedirect(reverse('edit', args=[slug])
                                        + f"?query={request.GET.get('query')}")
        elif bulletin_form.is_valid():
            post = bulletin_form.save(commit=False)
            post.slug = slugify(post.title)
            post.author = request.user
            post.edited = True
            post.save()

            query = request.GET.get('query')

            if 'page=' in query:
                split_query = query.split('page=')

            if '/post/' not in request.GET.get('query'):
                if 'page=' in query:
                    messages.success(request, 'You edited your bulletin.')
                    return HttpResponseRedirect(f'/?page={split_query[1]}')
                elif '/edit_comment/' in query:
                    messages.success(request, 'You edited your bulletin.')
                    return HttpResponseRedirect(reverse('bulletin',
                                                args=[post.slug]))
                else:
                    messages.success(request, 'You edited your bulletin.')
                    return HttpResponseRedirect(reverse('home'))
            else:
                messages.success(request, 'You edited your bulletin.')
                return HttpResponseRedirect(reverse('bulletin',
                                            args=[post.slug]))
        else:
            messages.error(request, 'This title has already been used. ' +
                           'Please choose another.')

            return HttpResponseRedirect(reverse('edit', args=[slug])
                                        + f"?query={request.GET.get('query')}")


class DeleteBulletin(View):
    """
    This is the view used for the deletion of bulletins.
    It only requires a post method, as the frontend
    requirements for this operation are minimal.
    """
    def post(self, request, slug, *args, **kwargs):
        """
        This is the post method for the delete view.
        It is triggered when you click the delete button,
        which can be found on the main page, or on the page
        for a specific bulletin. However, regardless
        of where the user clicks this button, they
        will be redirected to the main page once the
        below code completes execution. They cannot
        be redirected to the bulletin page itself,
        as the bulletin will have just been deleted.

        As with the edit functionality, the delete functionality
        has two layers of protection. The button is only
        visible on bulletins made by the user, and they
        must be logged in, and secondly, non-registered
        users cannot successfully delete a bulletin
        by navigating to a delete url pattern because
        of my use of get_object_or_404 and author=request.user.
        """
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug,
                                     author=request.user)

        bulletin.delete()

        messages.success(request, 'You deleted your bulletin.')

        return HttpResponseRedirect(reverse('home'))


class BulletinLike(View):
    """
    This is the view that handles the like functionality
    for bulletins. As with the delete view, this view only
    requires a post method, as users do not need to be
    sent to another page to like a bulletin.
    """
    def post(self, request, slug, *args, **kwargs):
        """
        This is the post method that handles liking and unliking
        a bulletin. As any registered user can like any bulletin,
        I did not use author=request.user in the call to
        get_object_or_404. Doing so would have restricted them
        to liking only their own posts! Not to mention they would
        have been presented with a 404 page every time they
        attempted to like someone else's post.

        However, the like functionality should only be available
        to registered users. In the template, the like button
        is only visible to registered users, but that doesn't
        stop them from navigating to a url pattern. So, at the
        view level, I have added another check to see if the
        user is authenticated, and the like code only executes
        if they are. Otherwise, they are shown a 404 page.

        The like code itself first adds the current user to the
        likes/users bridge table for the given bulletin if they
        aren't already on it, and removes them if they are.
        At the template level, this determines the appearance
        of the like button, and of course the number of likes
        the bulletin has.

        As with the edit bulletin view, there is code to return
        the user to whichever page they liked the bulletin from,
        as it is possible to like a bulletin from both the main
        page and the bulletins own page.
        """
        if request.user.is_authenticated:
            queryset = Bulletin.objects.filter(status=1)
            bulletin = get_object_or_404(queryset, slug=slug)

            if bulletin.likes.filter(id=request.user.id).exists():
                bulletin.likes.remove(request.user)
            else:
                bulletin.likes.add(request.user)

            query = request.GET.get('query')

            if 'page=' in query:
                split_query = query.split('page=')

            if '/post/' not in request.GET.get('query'):
                if 'page=' in query:
                    return HttpResponseRedirect(f'/?page={split_query[1]}')
                elif '/edit_comment/' in query:
                    return HttpResponseRedirect(reverse('bulletin',
                                                        args=[slug]))
                else:
                    return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseRedirect(reverse('bulletin', args=[slug]))
        else:
            raise Http404


class EditComment(View):
    """
    This is the view that enables users to edit comments
    that they leave on bulletins. It has both a get and a post
    method in order to display the comment being edited
    in the comment form, and to enable submission of that
    forms data.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        This is the get method for the edit comment page,
        which is actually just the bulletin detail page,
        but with a comment form pre-populated with the comment
        that the user wishes to edit.

        Therefore, it does everything that the bulletin view
        does (see above), whilst also populating said form.

        To prevent non-registered users from editing comments,
        get_object_or_404 looks for the comment with the given
        id by the currently logged in user. Again, if the user
        is anonymous, they will be shown a 404 page at this point.

        This user check is not used when querying for the current
        bulletin, as, similar to in the like view (see above)
        this would prevent the user from leaving comments on
        bulletins that they themselves did not post.

        Note that comments do not have slugs, as per the Comment
        model, so their id values are used in queries instead,
        hence the reason that a given comments id is attached
        via query to the url pattern for this view.
        """
        bulletin_queryset = Bulletin.objects.filter(status=1)
        specific_bulletin = get_object_or_404(bulletin_queryset, slug=slug)

        comments = (Comment.objects.filter(bulletin=specific_bulletin)
                    .annotate(likes_temp=Max('likes'))
                    .order_by(F('likes_temp')
                    .desc(nulls_last=True)))

        query = request.GET.get('query')
        comment = get_object_or_404(comments, id=query, author=request.user)

        comment_form = CommentForm(instance=comment)

        return render(
            request,
            'bulletin.html',
            {
                'bulletin': specific_bulletin,
                'comments': comments,
                'comment_form': comment_form,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        This is the post method for the edit comment view.
        It is similar to the edit bulletin view in many ways,
        once again only finding the comment to update if it
        was created by the current user.

        However, there are three lines towards the beginning
        that only appear here, and nowhere else. When the user
        clicks the edit button beside their comment, the URL
        that is generated has a query string attached that
        is set to the comments id. That URL looks something like:
        'edit_comment/bulletin-1/?query=1', and it triggers the
        get method above.

        If you look at the comment form code in bulletin.html,
        you will see that there is an if-else within it.
        This if-else determines the action attribute of said
        form. If 'edit_comment' is in the current page URL,
        then the form submits to the edit_comment url pattern
        and attaches as a query string the current url, which
        looks like:
        edit_comment/bulletin-1/?query=edit_comment/bulletin-1/?query=1

        The post method needs the id of the comment being edited,
        so it extracts this from the query of the URL that posted
        to it using the split method.

        This was necessary because comment objects are not
        accessible from within the comment form. I had to pass
        data around using query strings.
        """
        queryset = Bulletin.objects.filter(status=1)
        specific_bulletin = get_object_or_404(queryset, slug=slug)

        query = request.GET.get('query')
        split_query = query.split('=')
        comment_id = split_query[1]

        comments = (Comment.objects.filter(bulletin=specific_bulletin)
                    .annotate(likes_temp=Max('likes'))
                    .order_by(F('likes_temp')
                    .desc(nulls_last=True)))

        comment = get_object_or_404(comments, id=comment_id,
                                    author=request.user)

        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment.comment == comment_form.data['comment']:
            messages.warning(request, "You didn't make any changes " +
                             "to your comment...")

            return HttpResponseRedirect(reverse('comment_edit', args=[slug])
                                        + f'?query={comment_id}')
        elif comment_form.is_valid():
            post = comment_form.save(commit=False)
            post.author = request.user
            post.edited = True
            post.save()

            messages.success(request, 'You edited your comment.')

            return HttpResponseRedirect(reverse('bulletin', args=[slug]))


class DeleteComment(View):
    """
    This is the view used for deleting comments. As with bulletins,
    deletion is just an operation that happens on the backend,
    and is triggered by a button on a given bulletin's page.
    """
    def post(self, request, slug, *args, **kwargs):
        """
        Similar to all of the comment-related views above,
        the user is validated only for the query made against
        the Comment table, and not for the query made against
        the Bulletin table. This prevents anonymous users from
        deleting comments by navigating to a delete comment
        url pattern, and also enables registered users to delete
        comments they have made on other users' bulletins.

        Upon deleting a comment, the user is quietly redirected
        to the page of the bulletin on which they originally
        left the comment. All that is needed to do complete
        the url pattern for this page is the slug of the given
        bulletin.

        Similarly to other buttons mentioned above, the delete
        button is only visible on comments made by the user
        who is logged in.
        """
        queryset = Bulletin.objects.filter(status=1)
        specific_bulletin = get_object_or_404(queryset, slug=slug)

        comment_id = request.GET.get('query')

        comments = (Comment.objects.filter(bulletin=specific_bulletin)
                    .annotate(likes_temp=Max('likes'))
                    .order_by(F('likes_temp')
                    .desc(nulls_last=True)))

        comment = get_object_or_404(comments, id=comment_id,
                                    author=request.user)

        comment.delete()

        messages.success(request, 'You deleted your comment.')

        return HttpResponseRedirect(reverse('bulletin', args=[slug]))


class CommentLike(View):
    """
    This is the view for the comment liking / unliking functionality.
    As with the same view for bulletins, this view only requires
    a post method.
    """
    def post(self, request, slug, *args, **kwargs):
        """
        This is the post method for the comment like view.
        It uses many of the same techniques used in the other views
        above.

        To prevent non-registered users from navigating to the url
        pattern for this view, the view code is wrapped in a user-
        validating if-else. In the template, the like button is
        non-functional to anonymous users.

        As mentioned above in the edit comment view, the comment
        being like is gotten via its id, which is passed to
        the view via a query string attached to the url pattern.

        As in the bulletin like view, the user is added to the
        likes/users bridge table if they aren't found in it,
        and removed if they are, and in the template, whether
        they are in this table determines the look of the like
        button.
        """
        if request.user.is_authenticated:
            bulletin_queryset = Bulletin.objects.filter(status=1)
            specific_bulletin = get_object_or_404(bulletin_queryset, slug=slug)

            comments = Comment.objects.filter(bulletin=specific_bulletin)
            query = request.GET.get('query')
            comment = get_object_or_404(comments, id=query)

            if comment.likes.filter(id=request.user.id).exists():
                comment.likes.remove(request.user)
            else:
                comment.likes.add(request.user)

            return HttpResponseRedirect(reverse('bulletin', args=[slug]))
        else:
            raise Http404


def handler404(request, exception):
    """
    This is a function-based implementation of Django's 404
    handler. I am using it here to display a custom error page
    for 404 errors. These pages display when these errors
    are thrown, but only when debug is set to False in settings.py.
    """
    return render(request, '404.html', status=404)


def handler500(request):
    """
    This is a function-based implementation of Django's 500
    handler. I am using it here to display a custom error page
    for 500 errors. These pages display when these errors
    are thrown, but only when debug is set to False in settings.py.
    """
    return render(request, '500.html', status=500)
