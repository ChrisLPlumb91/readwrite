from . import views
from django.urls import path


urlpatterns = [
     path('', views.BulletinList.as_view(), name='home'),
     path('add', views.AddBulletin.as_view(), name='add'),
     path('post/<slug:slug>/', views.BulletinDetail.as_view(),
          name='bulletin'),
     path('edit/<slug:slug>/', views.EditBulletin.as_view(), name='edit'),
     path('confirm_delete/<slug>/', views.DeleteBulletin.as_view(),
          name='confirm_delete'),
     path('like/<slug:slug>', views.BulletinLike.as_view(),
          name='bulletin_like'),
     path('edit_comment/<slug:slug>', views.EditComment.as_view(),
          name='comment_edit'),
     path('delete_comment/<slug:slug>', views.DeleteComment.as_view(),
          name='comment_delete'),
     path('comment_like/<slug:slug>', views.CommentLike.as_view(),
          name='comment_like'),
]