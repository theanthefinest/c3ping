from django.urls import path
from . import views
from .views import recommend_page, KNN_RecommendAPIView, analytics, profile
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', recommend_page, name='recommend'),
    path('profile', views.profile, name="profile"),
    path('analytics/', views.analytics, name="analytics"),
    path('distribution/',views.distribution, name="distribution"),
    path('api/recommend/knn/', KNN_RecommendAPIView.as_view(), name='recommend-knn'),
]