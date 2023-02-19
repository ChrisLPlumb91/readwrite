from . import views
from django.urls import path


urlpatterns = [
    path('', views.BulletinList.as_view(), name='home'),
    path('add', views.AddBulletin.as_view(), name='add'),
    path('<slug:slug>/', views.BulletinDetail.as_view(), name='bulletin'),
]