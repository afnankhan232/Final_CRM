# ---- ==== Import Statement Goes HERE ==== ----

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# A helper notification section, which notify the new activity
from django.contrib import messages

from client.models import Contact, Project
from client.forms import ProjectCreationForm



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

    print(request.user)

    # Project Creation!!
    if(request.method == "POST"):
        # After work
        # Check if the From is from ProjectCreation OR ClientCreation

        form = ProjectCreationForm(request.POST, user=request.user)
        if(form.is_valid()):
            # Commit as False -> cause we need other field to be enter before saving the form
            projectValidForm = form.save(commit = False)
            projectValidForm.user = request.user
            projectValidForm.save() # Save the form

            messages.success(request, f"New Project Created Successfully!")

            return redirect('appContacts')
        
        else:
            # Message for un-success project creation
            messages.error(request, "A project with this name already exists.")
            return redirect('appContacts')
    else:
        form = ProjectCreationForm(user=request.user)

    # current User
    user = request.user

    # some Values from DATABASE [existing user]
    contacts = Contact.objects.filter(owner=user)
    projects = Project.objects.filter(user=user)

    context = {
        'form': form,
        'contacts': contacts,
        'projects': projects,
        'total_contacts': contacts.count(),
    }

    return render (
        request, 
        'featuredApp/contacts.html', 
        context,
    )

@login_required
def tasks_view(request, *args, **kwargs):
    return render(request, 'featuredApp/tasks.html')

@login_required
def activities_view(request, *args, **kwargs):
    return render(request, 'featuredApp/activities.html')

