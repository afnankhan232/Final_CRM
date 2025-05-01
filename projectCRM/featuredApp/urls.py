from django.urls import path
from . import views

urlpatterns = [

    # Dashboard considered as the home
    path('dashboard/', views.dashboard_view, name='appDashboard'),

    # Contains trusted Clients ( - )
    path('contacts/', views.contact_view, name='appContacts'),

    # Task - Calendar; Notification; and more!
    path('tasks/', views.tasks_view, name='appTasks'),

    # Documents - add your documents
    path('documents/', views.documents_view, name='appDocuments'),

    # ??
    path('activities/', views.activities_view, name='appActivities'),
    
]