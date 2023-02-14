from . import views
from django.urls import path


urlpatterns = [
    path('', views.BulletinList.as_view(), name='home'),
]