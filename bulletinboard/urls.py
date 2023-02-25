from . import views
from django.urls import path


urlpatterns = [
     path('', views.BulletinList.as_view(), name='home'),
     path('add', views.AddBulletin.as_view(), name='add'),
     path('post/<slug:slug>/', views.BulletinDetail.as_view(), name='bulletin'),
     path('edit/<slug:slug>/', views.EditBulletin.as_view(), name='edit'),
     path('post_delete/<slug>', views.ConfirmDeleteBulletin.as_view(),
          name="post_delete"),
     path('delete/<slug:slug>/', views.BulletinListAlt.as_view(),
          name='home_alt'),
     path('delete_bulletin/<slug:slug>/<int:comment_id>',
          views.BulletinDetailAlt.as_view(), name='post_alt'),
     path('confirm_delete/<slug>/', views.DeleteBulletin.as_view(),
          name='confirm_delete'),
     path('like/<slug:slug>', views.BulletinLike.as_view(),
          name='bulletin_like'),
     path('edit_comment/<slug:slug>', views.EditComment.as_view(),
          name='comment_edit'),
     path('comment_delete_request/<slug:slug>',
          views.ConfirmDeleteComment.as_view(),
          name='delete_request'),
     path('delete_comment/<slug:slug>', views.DeleteComment.as_view(),
          name='comment_delete'),
     path('comment_like/<slug:slug>', views.CommentLike.as_view(),
          name='comment_like'),
]