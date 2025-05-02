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
    # List View Clients ( - )
    path('contacts/', views.contact_view, name='appContacts'),

    # Detailed View of Clients
    path('contacts/<int:pk>/', views.contact_detailed_view, name='appContactDetail'),

    # Delete of Clients
    path('contacts/<int:pk>/delete', views.contact_delete_view, name='appContactDelete'),

    # Permanent Delete of Client
    path('contacts/<int:pk>/permanentDelete', views.contact_permanent_delete_view, name='appContactPermanentDelete'),

    # Restore of Client
    path('contacts/<int:pk>/restore', views.contact_restore_view, name='appContactRestore'),


    # ---- ==== Related to Tasks ==== ----
    # Task - Calendar; Notification; and more!
    path('tasks/', views.tasks_view, name='appTasks'),

    # ---- ==== Related to Documents ==== ----
    # Documents List View
    path('documents/', views.documents_view, name='appDocuments'),

    # ??
    path('activities/', views.activities_view, name='appActivities'),


    # Trash - Contain Trash - that no-one likes, but save lives!
    path('trash/', views.trash_view, name='appTrash'),
]