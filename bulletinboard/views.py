from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Bulletin, Comment
from .forms import BulletinForm, CommentForm


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


class AddBulletin(View):
    def get(self, request):

        return render(
            request,
            'add_bulletin.html',
            {
                'bulletin_form': BulletinForm()
            },
        )
        
    def post(self, request, slug, *args, **kwargs):
        bulletin_form = BulletinForm(data=request.POST)

        if bulletin_form.is_valid():
            bulletin_form.instance.author = request.user.username
            bulletin_form.save()
        else:
            bulletin_form = BulletinForm()

        queryset = Bulletin.objects.filter(status=1)
        bulletin = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            'bulletin.html',
            {
                'bulletin': bulletin,
                'comment_form': CommentForm(),
            }
        )


