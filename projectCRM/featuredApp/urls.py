from django.urls import path
from . import views

urlpatterns = [

    # Dashboard considered as the home
    path('dashboard/', views.dashboard_view, name='appDashboard'),

    # Contains trusted leads
    path('contacts/', views.contact_view, name='appContacts'),

    # Task - Calendar; Notification
    path('tasks/', views.tasks_view, name='appTasks'),

    # ??
    path('activities/', views.activities_view, name='appActivities'),
    
]