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
    path('delete_bulletin/<slug:slug>/', views.BulletinDetailAlt.as_view(),
         name='post_alt'),
    path('confirm-delete/<slug>/', views.DeleteBulletin.as_view(),
         name='confirm_delete'),
    path('like/<slug:slug>', views.BulletinLike.as_view(), name='bulletin_like'),
]