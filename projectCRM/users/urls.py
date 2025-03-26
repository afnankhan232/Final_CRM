from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='user-home'),
    path('myCompany/', views.home, name='user-home-page'),
    path('about/', views.about, name='user-about')
]