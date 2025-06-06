from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [

    # Just the default 
    path('', lambda request: redirect('/apps/dashboard/', permanent=False)),

    # ---- ==== Switch Account ==== ----
    path('switch-account/<uuid:public_id>/', views.switch_account, name='switch_account'),

    # ---- ==== Related to Dashboard ==== ----
    # Dashboard considered as the home
    path('dashboard/', views.dashboard_view, name='appDashboard'),


    # ---- ==== Related to Clients && Project(List) ==== ----
    # List View Clients
    path('contacts/', views.contact_view, name='appContacts'),
    # Detailed View of Clients
    path('contacts/<int:pk>/', views.contact_detailed_view, name='appContactDetail'),
    # Deletion Clients
    path('contacts/<int:pk>/delete/', views.contact_delete_view, name='appContactDelete'),
    # Permanent Deletion of Client
    path('contacts/<int:pk>/permanentDelete/', views.contact_permanent_delete_view, name='appContactPermanentDelete'),
    # Restoring Deleted Client
    path('contacts/<int:pk>/restore/', views.contact_restore_view, name='appContactRestore'),
    # Delete Project
    path('list/<str:name>/delete/', views.project_delete_view, name='appProjectDelete'),
    # Permenent Deletion of Project
    path('list/<int:id>/permanentDelete/', views.project_permanent_delete_view, name='appProjectPermanentDelete'),
    # Restoring Deleted Project
    path('list/<int:id>/restore/', views.project_restore_view, name='appProjectRestore'),

    # ---- ==== Related to Tasks ==== ----
    # Task - Calendar; Notification; and more!
    path('tasks/', views.tasks_view, name='appTasks'),
    # Detailed Tasks
    path('tasks/detail/<int:pk>/', views.task_detailed_view, name='appTaskDetail'),
    # Mark as Completed
    path('tasks/detail/<int:pk>/mark_complete/', views.task_mark_completed_view, name='appTaskMarkComplete'),
    # Delete Task
    path('tasks/detail/<int:pk>/delete/', views.task_delete_view, name='appTaskDelete'),
    # Restore Task
    path('tasks/<int:pk>/restore/', views.task_restore_view, name='appTaskRestore'),
    # Permanent Delete Task
    path('tasks/<int:pk>/permanent-delete/', views.task_permanent_delete_view, name='appTaskPermanentDelete'),

    # ---- ==== Related to Documents ==== ----
    # Documents List View
    path('documents/', views.documents_view, name='appDocuments'),
    # Document Detailed View
    path('document/detail/<int:pk>/', views.documents_detailed_view, name='appDocumentDetail'),
    # Delete Document
    path('document/delete/<int:pk>/', views.document_delete_view, name='appDocumentDelete'),
    # Restore Document
    path('document/permanentDelete/<int:pk>/', views.document_permanent_delete_view, name='appDocumentPermanentDelete'),
    # Permanent Delete Document
    path('document/restore/<int:pk>/', views.document_restore_view, name='appDocumentRestore'),

    # ---- ==== Related to Activities ==== ----
    path('activities/', views.activities_view, name='appActivities'),


    # ---- ===== Related to Trash ==== ----
    # Trash - Contain Trash - that no-one likes, but save lives!
    path('trash/', views.trash_view, name='appTrash'),

    # ---- ==== Manage Access : Multiple Users ==== ----
    path('manage-access/', views.manage_access, name='appManageAccess'),
    path('manage-access/delete-role/<int:role_id>/', views.delete_role, name='delete_role'),
    path('manage-access/delete-access/<int:access_id>/', views.delete_access, name='delete_access'),

    # ---- ==== Send Feedback ==== ----
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
]