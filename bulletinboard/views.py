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
    model = Bulletin
    queryset = Bulletin.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 10


class BulletinDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        specific_bulletin = get_object_or_404(queryset, slug=slug)
        comments = Comment.objects.filter(bulletin=specific_bulletin).annotate(likes_temp=Max('likes')).order_by(F('likes_temp').desc(nulls_last=True))

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
        queryset = Bulletin.objects.filter(status=1)
        specific_bulletin = get_object_or_404(queryset, slug=slug)
        comments = Comment.objects.filter(bulletin=specific_bulletin).annotate(likes_temp=Max('likes')).order_by(F('likes_temp').desc(nulls_last=True))
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.bulletin = specific_bulletin
            comment.author = request.user
            comment.save()
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


class AddBulletin(View):
    def get(self, request):

        if (request.user.is_authenticated):
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
            messages.error(request, 'This title has already been used. Please choose another.')
            return render(
                request,
                'add_bulletin.html',
                {
                    'bulletin_form': bulletin_form
                },
            )


class EditBulletin(View):
    def get(self, request, slug, *args, **kwargs):
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
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)

        bulletin_form = BulletinForm(data=request.POST, instance=bulletin)

        print(bulletin.title == bulletin_form.data['title'])

        if bulletin.title == bulletin_form.data['title'] and bulletin.content == bulletin_form.data['content'] and bulletin.link == bulletin_form.data['link']:
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

            if '/post/' not in request.GET.get('query'):
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
    def post(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug,
                                     author=request.user)
        bulletin.delete()

        messages.success(request, 'You deleted your bulletin.')
        return HttpResponseRedirect(reverse('home'))


class BulletinLike(View):
    def post(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)

        if bulletin.likes.filter(id=request.user.id).exists():
            bulletin.likes.remove(request.user)
        else:
            bulletin.likes.add(request.user)

        if '/post/' not in request.GET.get('query'):
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('bulletin', args=[slug]))


class EditComment(View):
    def get(self, request, slug, *args, **kwargs):
        bulletin_queryset = Bulletin.objects.filter(status=1)
        specific_bulletin = get_object_or_404(bulletin_queryset, slug=slug)

        comments = Comment.objects.filter(bulletin=specific_bulletin).annotate(likes_temp=Max('likes')).order_by(F('likes_temp').desc(nulls_last=True))
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
        queryset = Bulletin.objects.filter(status=1)
        specific_bulletin = get_object_or_404(queryset, slug=slug)

        query = request.GET.get('query')
        split_query = query.split('=')
        comment_id = split_query[1]

        comments = Comment.objects.filter(bulletin=specific_bulletin).annotate(likes_temp=Max('likes')).order_by(F('likes_temp').desc(nulls_last=True))
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
    def post(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        print(slug)
        specific_bulletin = get_object_or_404(queryset, slug=slug)

        comment_id = request.GET.get('query')
        comments = Comment.objects.filter(bulletin=specific_bulletin).annotate(likes_temp=Max('likes')).order_by(F('likes_temp').desc(nulls_last=True))
        comment = get_object_or_404(comments, id=comment_id,
                                    author=request.user)

        comment.delete()

        messages.success(request, 'You deleted your comment.')
        return HttpResponseRedirect(reverse('bulletin', args=[slug]))


class CommentLike(View):
    def post(self, request, slug, *args, **kwargs):
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


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
