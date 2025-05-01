# ---- ==== Import Statement Goes HERE ==== ----

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# A helper notification section, which notify the new activity
from django.contrib import messages

from client.models import Client
from client.forms import ClientCreationForm

# Project Model and Form
from client.models import Project
from client.forms import ProjectCreationForm

# Document model and form 
from client.models import Document
from client.forms import DocumentCreationForm


# ---- ==== Pofile link (containing form to update existing information) ==== ----
@login_required
def profile(request, *args, **kwargs):
    return render(request, 'users/profile.html')

# ---- ==== FEATURED APP LINKS LISTED BELOW ==== ----
@login_required
def dashboard_view(request, *args, **kwargs):
    return render(request, 'featuredApp/dashboard.html')

@login_required
def contact_view(request, *args, **kwargs):

    # Project Creation!!
    if(request.method == "POST"):
        # After work
        # Check if the From is from ProjectCreation OR ClientCreation

        # the user arguement pass to the __init__ attribute of the ProjectCreationForm (it's no big deal)
        form = ProjectCreationForm(request.POST, user=request.user)
        if(form.is_valid()):
            # Commit as False -> cause we need other field to be enter before saving the form
            projectValidForm = form.save(commit = False)
            projectValidForm.user = request.user
            projectValidForm.save() # Save the form

            # A success Message
            messages.success(request, f"New Project Created Successfully!")

            return redirect('appContacts')
        
        else:
            # An error message
            messages.error(request, "A project with this name already exists.")

            # The re-direction help! - [ don't know if it's best practice! ]
            return redirect('appContacts')
    else:
        form = ProjectCreationForm(user=request.user)

    # current User
    user = request.user

    # Retrieving Values from DATABASE [current user]
    user = request.user
    project_id = request.GET.get('project_id')

    contacts = Client.objects.filter(companyAssignee=user)
    projects = Project.objects.filter(user=user)

    if project_id:
        contacts = contacts.filter(list__id = project_id)

    context = {
        'form': form,
        'contacts': contacts,
        'projects': projects,
        'total_contacts': contacts.count(),
        'selected_project_id': int(project_id) if project_id else None,
        'set_to_all': True if project_id is None else False,
    }

    return render (
        request, 
        'featuredApp/contacts.html', 
        context,
    )

@login_required
def tasks_view(request, *args, **kwargs):

    if request.method == "POST":
        form = ClientCreationForm(request.POST, user = request.user)
        if(form.is_valid()):
            tmp = form.save(commit = False)
            tmp.companyAssignee = request.user
            tmp.save()
            return redirect('appTasks')
    else:
        form = ClientCreationForm(user = request.user)

    return render(
        request, 
        'featuredApp/tasks.html',
        {
            'form': form,
        },
    )

@login_required
def documents_view(request, *args, **kwargs):

    if request.method == "POST":

        # For the purpose of file upload - we need request.FILES [COOL]
        form = DocumentCreationForm(request.POST, request.FILES, user = request.user)

        if(form.is_valid()):
            tmp = form.save(commit = False)
            tmp.user = request.user
            tmp.save()

            messages.success(request, f"New Document Added!")
            return redirect('appDocuments')
        else:

            messages.success(request, f"Something Went Wrong!")
            return redirect('appDocuments')
    else:
        form = DocumentCreationForm(user = request.user)

    # Retrieving Values from DATABASE [current user]
    user = request.user

    documents = Document.objects.filter(user=user)

    return render(
        request, 
        'featuredApp/documents.html',
        {
            "documents": documents, 
            'total_documents': documents.count(), 
            "form": form,
        }
    )

@login_required
def activities_view(request, *args, **kwargs):
    return render(request, 'featuredApp/activities.html')

