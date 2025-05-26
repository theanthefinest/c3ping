from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend', views.recommend_view, name='recommend'),
    path('profile', views.profile, name="profile"),
    path('analytics', views.analytics, name="analytics"),
]