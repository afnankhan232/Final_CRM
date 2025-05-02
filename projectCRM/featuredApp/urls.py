from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [

    # Just the default 
    path('', lambda request: redirect('/apps/dashboard/', permanent=False)),

    # ---- ==== Related to Dashboard ==== ----
    # Dashboard considered as the home
    path('dashboard/', views.dashboard_view, name='appDashboard'),


    # ---- ==== Related to Clients ==== ----
    # Contains trusted Clients ( - )
    path('contacts/', views.contact_view, name='appContacts'),

    # Detailed View of Clients
    path('contacts/<int:pk>/', views.contact_detailed_view, name='appContactDetail'),

    # Delete View of Clients
    path('contacts/<int:pk>/delete', views.contact_delete_view, name='appContactDelete'),


    # ---- ==== Related to Tasks ==== ----
    # Task - Calendar; Notification; and more!
    path('tasks/', views.tasks_view, name='appTasks'),

    # Documents - add your documents
    path('documents/', views.documents_view, name='appDocuments'),

    # ??
    path('activities/', views.activities_view, name='appActivities'),
    
]