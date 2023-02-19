from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
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
        liked = False

        if bulletin.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'bulletin.html',
            {
                'bulletin': bulletin,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)
        comments = bulletin.comments_on_post.order_by('created_on')
        liked = False

        if bulletin.likes.filter(id=self.request.user.id).exists():
            liked = True

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
                'commented': True,
                'liked': liked,
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
        else:
            bulletin_form = BulletinForm()

        return redirect('home')