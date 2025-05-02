# ---- ==== Import Statement Goes HERE ==== ----

from django.shortcuts import render, redirect, get_object_or_404
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

# Date Time Field
from django.utils import timezone


# ---- ==== Profile link (containing form to update existing information) ==== ----
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

        # Possible Values: ['project_form', 'client_form']
        form_type = request.POST.get("form_type")

        # Handeling two different form off one view
        if(form_type == 'project_form'):

            # the user arguement pass to the __init__ attribute of the ProjectCreationForm (it's no big deal)
            formA = ProjectCreationForm(request.POST, user = request.user)
            formB = ClientCreationForm(user = request.user)

            if(formA.is_valid()):
                # Commit as False -> cause we need other field to be enter before saving the form
                projectValidForm = formA.save(commit = False)
                projectValidForm.user = request.user
                projectValidForm.save() # Save the form

                # A success Message
                messages.success(request, f"New Project Created Successfully!")

                return redirect('appContacts')
            
            else:
                messages.error(request, "Project Name should be unique!")

                # For development
                print("Form errors:", formA.errors)

                return redirect('appContacts')
                

        elif(form_type == 'client_form'):

            formA = ProjectCreationForm(user = request.user)
            # the user arguement pass to the __init__ attribute of the ProjectCreationForm (it's no big deal)
            formB = ClientCreationForm(request.POST, user = request.user)

            if(formB.is_valid()):
                clientValidForm = formB.save(commit = False)
                clientValidForm.companyAssignee = request.user
                clientValidForm.save()
                
                # A success Message
                messages.success(request, f"New Client Created Successfully!")

                return redirect('appContacts')
            
            else:
                messages.error(request, "PhoneNumber or Email should be provided for Client")

                # For Development
                print("Form errors:", formB.errors)

                return redirect('appContacts')
            
            
    else:
        formA = ProjectCreationForm(user = request.user)
        formB = ClientCreationForm(user = request.user)

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
        'formA': formA,
        'formB': formB,
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
def contact_detailed_view(request, pk):

    # filtering specific contact -> [Current User] [Current Client]
    contact = get_object_or_404(Client, companyAssignee = request.user, pk=pk)

    # Client Updation Form
    if(request.method == "POST"):
        formEditClient = ClientCreationForm(request.POST, user = request.user, instance = contact)

        if(formEditClient.is_valid()):
            formEditClient.last_edit = timezone.now()
            formEditClient.save()
            messages.success(request, "Client information Updated!")
            return redirect('appContactDetail', pk=pk)

        else:
            messages.error(request, "Can't edit the user detail!")
            return redirect('appContactDetail', pk=pk)
    else:
        formEditClient = ClientCreationForm(user = request.user, instance = contact)

    context = {
        'contact': contact,
        'form': formEditClient,
    }

    return render(
        request,
        'featuredApp/contact_detailed.html',
        context,
    )

@login_required
def contact_delete_view(request, pk):

    # Only POST request delete the form and not the GET request!
    if(request.method == "POST"):
        contact = get_object_or_404(Client, companyAssignee = request.user, pk=pk)
        contact_name = contact.name

        try:
            contact.soft_delete()
            messages.success(request, f"Client '{contact_name}' is deleted!")
        except Exception as err:
            print(err)
            messages.error(request, f"Can't Delete Client '{contact_name}' ")
    else:
        messages.error(request, f"GET Request is not allowed for this page!")

    return redirect('appContacts')


@login_required
def contact_permanent_delete_view(request, pk):

    print("I am right here")

    # Only POST request delete the form and not the GET request!
    if(request.method == "POST"):

        print("Get into POST request ")
        contact = get_object_or_404(Client.all_objects, companyAssignee = request.user, pk=pk)
        print("Gather contact Data Instance")
        contact_name = contact.name

        try:
            contact.delete()
            messages.success(request, f"Client '{contact_name}' is deleted permanently!")
            
        except Exception as err:
            print(err)
            messages.error(request, f"Can't Delete Client '{contact_name}' ")
    else:
        messages.error(request, f"GET Request is not allowed for this page!")

    return redirect('appTrash')


@login_required
def contact_restore_view(request, pk):

    if(request.method == "POST"):
        contact = get_object_or_404(Client.all_objects, companyAssignee = request.user, pk=pk)
        contact_name = contact.name

        try:
            contact.restore()
            messages.success(request, f"Restored Contact '{contact_name}")
        except Exception as err:
            print(err)
            messages.error(request, f"Can't Restore Contact '{contact_name}'")

    return redirect('appTrash')

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


@login_required
def trash_view(request):
    trashed_contacts = Client.all_objects.filter(companyAssignee = request.user, is_deleted = True)
    trashed_documents = Document.all_objects.filter(user = request.user, is_deleted = True)
    trashed_project = Project.all_objects.filter(user = request.user, is_deleted = True)

    return render(
        request,
        'featuredApp/trash.html',
        {
            'trashed_contacts': trashed_contacts,
        },
    )