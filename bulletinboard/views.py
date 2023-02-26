from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .models import Bulletin, Comment
from .forms import BulletinForm, CommentForm
from django.template.defaultfilters import slugify


class BulletinList(generic.ListView):
    model = Bulletin
    queryset = Bulletin.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 10


class BulletinDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)
        comments = bulletin.comments_on_post.order_by('likes')

        return render(
            request,
            'bulletin.html',
            {
                'bulletin': bulletin,
                'comments': comments,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)
        comments = bulletin.comments_on_post.order_by('created_on')

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.bulletin = bulletin
            comment.author = request.user
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            'bulletin.html',
            {
                'bulletin': bulletin,
                'comments': comments,
                'comment_form': CommentForm()
            },
        )


class AddBulletin(View):
    def get(self, request):

        return render(
            request,
            'add_bulletin.html',
            {
                'bulletin_form': BulletinForm()
            },
        )

    def post(self, request, *args, **kwargs):
        bulletin_form = BulletinForm(data=request.POST)

        if bulletin_form.is_valid():
            post = bulletin_form.save(commit=False)
            post.slug = slugify(post.title)
            post.author = request.user
            post.save()
            return redirect('home')
        else:
            bulletin_form = BulletinForm()
            return redirect('home')


class EditBulletin(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)

        bulletin_form = BulletinForm(instance=bulletin)

        return render(
            request,
            'edit_bulletin.html',
            {
                'bulletin_form': bulletin_form,
                'bulletin': bulletin,
                'query': request.GET.get('query'),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)

        bulletin_form = BulletinForm(data=request.POST, instance=bulletin)

        if bulletin_form.is_valid():
            post = bulletin_form.save(commit=False)
            post.slug = slugify(post.title)
            post.author = request.user
            post.save()
            return redirect('bulletin', slug=post.slug)
        else:
            bulletin_form = BulletinForm()
            return redirect('home')


class ConfirmDeleteBulletin(View):
    def post(self, request, slug, *args, **kwargs):
        comment_id = 0
        if '/post/' not in request.GET.get('query'):
            return HttpResponseRedirect(reverse('home_alt', args=[slug]))
        else:
            return HttpResponseRedirect(reverse('post_alt',
                                        args=[slug, comment_id]))


class BulletinListAlt(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        paginator = Paginator(queryset, 10)
        bulletin = get_object_or_404(queryset, slug=slug)
        comments = bulletin.comments_on_post.order_by('likes')

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'index_alt.html',
            {
                'bulletin_list': queryset,
                'specific_bulletin': bulletin,
                'comments': comments,
                'page_obj': page_obj,
            },
        )


class BulletinDetailAlt(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)

        comments = bulletin.comments_on_post.order_by('likes')

        if kwargs['comment_id'] > 0:
            comment = get_object_or_404(comments, id=kwargs['comment_id'])
        else:
            comment = kwargs['comment_id']

        return render(
            request,
            'bulletin_alt.html',
            {
                'bulletin': bulletin,
                'comments': comments,
                'comment': comment,
                'comment_form': CommentForm()
            },
        )


class DeleteBulletin(View):
    def post(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)
        bulletin.delete()

        return redirect('home')


class BulletinLike(View):
    def post(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)

        if bulletin.likes.filter(id=self.request.user.id).exists():
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
        bulletin = get_object_or_404(bulletin_queryset, slug=slug)

        comments = bulletin.comments_on_post.order_by('likes')
        query = request.GET.get('query')
        print(query)
        comment = get_object_or_404(comments, id=query)

        comment_form = CommentForm(instance=comment)

        return render(
            request,
            'bulletin.html',
            {
                'bulletin': bulletin,
                'comments': comments,
                'comment_form': comment_form,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)

        query = request.GET.get('query')
        split_query_1 = query.split('=')
        comment_id = split_query_1[1]
        print(comment_id)

        comments = bulletin.comments_on_post.order_by('likes')
        comment = get_object_or_404(comments, id=comment_id)

        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid():
            post = comment_form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('bulletin', args=[slug]))
        else:
            bulletin_form = BulletinForm()
            return HttpResponseRedirect(reverse('bulletin', args=[slug]))


class ConfirmDeleteComment(View):
    def post(self, request, slug, *args, **kwargs):
        comment_id = request.GET.get('query')
        return HttpResponseRedirect(reverse('post_alt', 
                                    args=[slug, comment_id]))


class DeleteComment(View):
    def post(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)

        comment_id = request.GET.get('query')
        comments = bulletin.comments_on_post.order_by('likes')
        comment = get_object_or_404(comments, id=comment_id)

        comment.delete()

        return HttpResponseRedirect(reverse('bulletin', args=[slug]))


class CommentLike(View):
    def post(self, request, slug, *args, **kwargs):
        bulletin_queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(bulletin_queryset, slug=slug)

        comments = bulletin.comments_on_post.order_by('likes')
        query = request.GET.get('query')
        comment = get_object_or_404(comments, id=query)

        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)

        return HttpResponseRedirect(reverse('bulletin', args=[slug]))

