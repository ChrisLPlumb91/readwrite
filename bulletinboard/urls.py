from . import views
from django.urls import path


urlpatterns = [
    path('', views.BulletinList.as_view(), name='home'),
    path('<slug:slug>/', views.BulletinDetail.as_view(), name='post'),
    path('add_bulletin', views.AddBulletin.as_view(), name='add'),
]