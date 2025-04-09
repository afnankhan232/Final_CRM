from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='dashboardHome'),
    path('tasks/', views.tasks_view, name='dashboardTasks'),
    path('activities/', views.activities_view, name='dashboardActivities'),
    path('contacts/', views.contact_view, name='dashboardContact'),
]