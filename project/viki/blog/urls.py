from django.urls import path
from . import views
urlpatterns = [
    path('', views.start, name='dash-home'),
    path('about/', views.UserReq_detail, name='dash-about'),
    # path('detail/', views.Snippet_detail, name='dash-detail'),
    path('detail/', views.Snippet_detail, name='dash-detail'),
    path('register/', views.register, name='dash-register'),
    path('login/', views.login, name='dash-login'),
    # path('result/', views.start, name='blog-result'),
]
