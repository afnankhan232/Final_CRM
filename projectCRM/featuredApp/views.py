# ---- ==== Import Statement Goes HERE ==== ----

# Basic
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# A helper notification section, which notify the new activity
from django.contrib import messages

# Client Model and Form
from client.models import Client
from client.forms import ClientCreationForm

# Project Model and Form
from client.models import Project
from client.forms import ProjectCreationForm

# Document model and form 
from client.models import Document
from client.forms import DocumentCreationForm

from client.models import ProjectAccessPermisssion

# Date Time Field
from django.utils import timezone

# MORE SECURITY
def get_active_business_user_with_permission(request, permission_field_name: str, show_err = None, fallback = False):
    """
    Verifies if the logged-in user has the required permission on the active business account.
    
    Args:
        request: The HTTP request object.
        permission_field_name: A string name of the permission field (e.g. "can_read_project").

    Returns:
        BusinessUser: the active_business_user object.

    Raises:
        PermissionDenied: if permission is not granted or not found.
        Success: Boolean Value
    """

    print('I am working fine!')

    logged_in_user = request.user.businessuser

    active_id = request.session.get('active_business_user_id')
    active_business_user = get_object_or_404(BusinessUser, id=active_id)

    print("3#" * 50)
    print(active_business_user)

    if logged_in_user == active_business_user:
        return (active_business_user, False)

    try:
        permission = AccessPermission.objects.get(
            owner=active_business_user,
            shared_with=logged_in_user
        )
        has_permission = getattr(permission.role, permission_field_name, False)

        if not has_permission:
            if(show_err == None):
                show_err = permission_field_name
            messages.error(request, f"You don't have '{show_err}' permission.")
            raise PermissionDenied(f"Missing permission: {permission_field_name}")
        return (active_business_user, True)

    except AccessPermission.DoesNotExist:
        messages.error(request, "Access permission not found. Reverting to own account.")
        request.session['active_business_user_id'] = logged_in_user.id
        return (logged_in_user, False)
    except Exception as e:
        print("Developement eRROR: ", e)

    # fallback
    if(fallback == True):
        request.session['active_business_user_id'] = logged_in_user.id
    
    return (active_business_user, False)

# ---- ==== Profile link (containing form to update existing information) ==== ----
@login_required
def profile_view(request, *args, **kwargs):

    user = request.user.businessuser

    try:
        request.session.get('active_business_user_id')
        
    except:
        # Don't remove these two lines!
        logged_in_user = request.user.businessuser
        request.session['active_business_user_id'] = logged_in_user.id

    context = {
        'businessuser': user,
    }

    return render(
        request, 
        'users/profile.html',
        context,
    )

# ---- ==== FEATURED APP LINKS LISTED BELOW ==== ----

# ---- ==== Featured Related to Dashboard View ==== ----
# Include: [dashboard_view; ]
@login_required
def dashboard_view(request, *args, **kwargs):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    try:
        request.session.get('active_business_user_id')
    except:
        # Don't remove these two lines!
        logged_in_user = request.user.businessuser
        request.session['active_business_user_id'] = logged_in_user.id
    accessible_accounts = user.accessible_accounts.select_related('owner', 'role')
    context = {
        'businessuser': user,
        'accessible_accounts': accessible_accounts,
        'self_account': user,
    }
    return render(
        request, 
        'featuredApp/dashboard.html',
        context,
    )

# ---- ==== Switch Account Logic ==== ----
from django.core.exceptions import PermissionDenied
from accounts.models import BusinessUser, AccessPermission

@login_required
def switch_account(request, public_id):
    logged_in_user = request.user.businessuser
    target_user = get_object_or_404(BusinessUser, public_id=public_id)
    # Trying to access own account
    if target_user == logged_in_user:
        request.session['active_business_user_id'] = logged_in_user.id
        messages.success(request, f"You are now accessing your account!")
        return redirect('appDashboard')
    # Check access permission
    has_access = AccessPermission.objects.filter(
        owner=target_user,
        shared_with=logged_in_user
    ).exists()
    if has_access:
        request.session['active_business_user_id'] = target_user.id
        messages.success(request, f"You are now accessing: {target_user.user.email}")
        return redirect('appDashboard')

    else:
        messages.error(request, "You do not have access to this account.")
        return redirect('appDashboard')

# ---- ===== Featured Related to Contact View ==== ----
# Include: [contact_view; contact_detailed_view; contact_delete_view; contact_delete_permanently_view; contact_restore_view;]
@login_required
def contact_view(request, *args, **kwargs):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_read_contact', show_err='Read')
    # Project Creation!!
    if(request.method == "POST"):
        # Possible Values: ['project_form', 'client_form']
        form_type = request.POST.get("form_type")
        # Handeling two different form off one view
        if(form_type == 'project_form'):
            # the user arguement pass to the __init__ attribute of the ProjectCreationForm (it's no big deal)
            formA = ProjectCreationForm(request.POST, user = user)
            formB = ClientCreationForm(user = user)
            if(formA.is_valid()):
                # managing AccessPermission!! - adding new contacts
                if(
                    active_business_user == logged_in_user or
                    (
                        active_business_user != logged_in_user and
                        get_active_business_user_with_permission(request, 'can_add_project', show_err='Add') == True
                    )
                ):
                    projectValidForm = formA.save(commit = False)
                    projectValidForm.user = active_business_user
                    projectValidForm.save() # Save the form
                    messages.success(request, f"New Project Created Successfully!")
                    return redirect('appContacts')
                else:
                    messages.error(request, "Project Name should be unique!")
                    return redirect('appContacts')
        elif(form_type == 'client_form'):
            formA = ProjectCreationForm(user = user)
            # the user arguement pass to the __init__ attribute of the ProjectCreationForm (it's no big deal)
            formB = ClientCreationForm(request.POST, user = user)
            if(formB.is_valid()):
                if(
                    active_business_user == logged_in_user or
                    (
                        active_business_user != logged_in_user and
                        get_active_business_user_with_permission(request, 'can_add_contact', show_err='Add')[1] == True
                    )
                ):
                    clientValidForm = formB.save(commit = False)
                    clientValidForm.companyAssignee = active_business_user
                    clientValidForm.save()
                    messages.success(request, f"New Client Created Successfully!")
            else:
                messages.error(request, "PhoneNumber or Email should be provided for Client")
                return redirect('appContacts')
    else:
        formA = ProjectCreationForm(user = user)
        formB = ClientCreationForm(user = user)
    # Retrieving Values from DATABASE [current user]
    if(active_business_user == logged_in_user):
        projects = Project.objects.filter(user = logged_in_user)
        contacts = Client.objects.filter(companyAssignee = logged_in_user)
    else:
        projects = Project.objects.filter(
            shared_project_permissions__shared_with = logged_in_user,
            shared_project_permissions__can_read_project = True,
            user = active_business_user,
        )
        contacts = Client.objects.filter(
            list__in = projects,
            companyAssignee=active_business_user,
        )
    # these two line must be checked!!
    project_id = request.GET.get('project_id')
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
        'businessuser': user,
    }
    return render (
        request, 
        'featuredApp/contacts.html', 
        context,
    )

@login_required
def contact_detailed_view(request, pk):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_read_contact', show_err='Contact Read')
    # Retrieving Values from DATABASE [current user / active user]
    if(active_business_user == logged_in_user):
        projects = Project.objects.filter(user = logged_in_user)
        contact = get_object_or_404(Client, companyAssignee = user, pk=pk)
    else:
        projects = Project.objects.filter(
            shared_project_permissions__shared_with = logged_in_user,
            shared_project_permissions__can_read_project = True,
            user = active_business_user,
        )
        contact = get_object_or_404(
            Client,
            list__in = projects,
            companyAssignee=active_business_user,
            pk=pk,
        )
    # Client Updation Form
    if(request.method == "POST"):
        formEditClient = ClientCreationForm(request.POST, user = active_business_user, possible_projects = projects, instance = contact)
        if(formEditClient.is_valid()):
            if(
                (active_business_user == logged_in_user) 
                or 
                (
                    active_business_user != logged_in_user and 
                    get_active_business_user_with_permission(request, 'can_edit_contact', show_err='Client Edit')[1] == True
                )
            ):
                formEditClient.last_edit = timezone.now()
                formEditClient.save()
                messages.success(request, "Client information Updated!")
                return redirect('appContactDetail', pk=pk)
        else:
            messages.error(request, "Can't edit the user detail!")
            return redirect('appContactDetail', pk=pk)
    else:
        formEditClient = ClientCreationForm(user = active_business_user, possible_projects = projects, instance = contact)
    context = {
        'contact': contact,
        'form': formEditClient,
        'businessuser': user,
    }
    return render(
        request,
        'featuredApp/contact_detailed.html',
        context,
    )

@login_required
def contact_delete_view(request, pk):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_delete_contact', show_err='Delete')

    print(active_business_user.company_email, is_success)
    # Only POST request to delete the contact and not the GET request!
    if(request.method == "POST"):
        if(logged_in_user != active_business_user):
            contact = get_object_or_404(Client, companyAssignee = active_business_user, pk=pk)
        else:
            contact = get_object_or_404(Client, companyAssignee = logged_in_user, pk=pk)
            contact_name = contact.name
            contact.soft_delete()
            messages.success(request, f"Client '{contact_name}' is deleted!")
    else:
        messages.error(request, f"GET Request is not allowed for this page!")
    return redirect('appContacts')

@login_required
def contact_permanent_delete_view(request, pk):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_permanent_delete_contact', show_err='Permanent Delete')
    # Only POST request delete the form and not the GET request!
    if(request.method == "POST"):
        if(logged_in_user != active_business_user):
            contact = get_object_or_404(Client.all_objects, companyAssignee = active_business_user, pk=pk)
        else:
            contact = get_object_or_404(Client.all_objects, companyAssignee = user, pk=pk)
        contact_name = contact.name
        contact.delete()
        messages.success(request, f"Client '{contact_name}' is deleted permanently!")
    else:
        messages.error(request, f"GET Request is not allowed for this page!")
    return redirect('appTrash')

@login_required
def contact_restore_view(request, pk):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_delete_contact', show_err='Restore')
    if(request.method == "POST"):
        if(logged_in_user != active_business_user):
            contact = get_object_or_404(Client.all_objects, companyAssignee = active_business_user, pk=pk)
        else:
            contact = get_object_or_404(Client.all_objects, companyAssignee = user, pk=pk)
        contact_name = contact.name
        contact.restore()
        messages.success(request, f"Restored Contact '{contact_name}")
    return redirect('appTrash')

# ---- ==== Featured Related to Tasks View ==== ----
# Include: [tasks_view; ]
@login_required
def tasks_view(request, *args, **kwargs):

    user = request.user.businessuser

    if request.method == "POST":
        form = ClientCreationForm(request.POST, user = user)
        if(form.is_valid()):
            tmp = form.save(commit = False)
            tmp.companyAssignee = user
            tmp.save()
            return redirect('appTasks')
    else:
        form = ClientCreationForm(user = user)

    return render(
        request, 
        'featuredApp/tasks.html',
        {
            'form': form,
        },
    )

# ---- ==== Featured Related to Documents View ==== ----
# Include: [document_view; ]
@login_required
def documents_view(request, *args, **kwargs):

    user = request.user.businessuser

    if request.method == "POST":

        # For the purpose of file upload - we need request.FILES [COOL]
        form = DocumentCreationForm(request.POST, request.FILES, user = user)

        if(form.is_valid()):
            tmp = form.save(commit = False)
            tmp.user = user
            tmp.save()

            messages.success(request, f"New Document Added!")
            return redirect('appDocuments')
        else:

            messages.success(request, f"Something Went Wrong!")
            return redirect('appDocuments')
    else:
        form = DocumentCreationForm(user = user)

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

# ---- ==== Featured Related to Activities View ==== ----
# Include: [activities_view; ]
@login_required
def activities_view(request, *args, **kwargs):
    return render(request, 'featuredApp/activities.html')

# ---- ==== Featured Related to Trash View ==== ----
# Include: [trash_view; ]
@login_required
def trash_view(request):

    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_id = request.session.get('active_business_user_id')
    active_business_user = get_object_or_404(BusinessUser, id=active_id)

    if(logged_in_user != active_business_user):
        if(get_active_business_user_with_permission(request, 'can_delete_contact', show_err='Contact Delete')):
            trashed_contacts = Client.all_objects.filter(companyAssignee = active_business_user, is_deleted = True)
        # if(get_active_business_user_with_permission(request, 'can_delete_project')):
        #     trashed_project = Project.all_objects.filter(user = active_business_user, is_deleted = True)
        if(get_active_business_user_with_permission(request, 'can_delete_documents', show_err='Document Delete')):
            trashed_documents = Document.all_objects.filter(user = active_business_user, is_deleted = True)
    else:
        trashed_contacts = Client.all_objects.filter(companyAssignee = user, is_deleted = True)
        # trashed_project = Project.all_objects.filter(user = user, is_deleted = True)
        trashed_documents = Document.all_objects.filter(user = user, is_deleted = True)

    context = {
        'trashed_contacts': trashed_contacts,
    }

    return render(
        request,
        'featuredApp/trash.html',
        context,
    )

# ---- ==== Manage User Access ==== ----
from accounts.forms import RolesCreationForm_Account
from client.forms import ProjectAccessPermissionForm_Client
@login_required
def manage_access(request, *args, **kwargs):
    formA = RolesCreationForm_Account()
    formB = ProjectAccessPermissionForm_Client()
    formC = None
    user = request.user.businessuser
    project_queryset = Project.objects.filter(user = user)
    context = {
        'formA': formA,
        'formB': formB,
        'project_queryset': project_queryset,
    }
    return render(
        request,
        'featuredApp/manage_access.html',
        context,
    )

# def role_permission_view(request):
#     active_business_user = get_active_business_user(request)

#     form = ProjectAccessPermissionForm()
#     project_queryset = Project.objects.filter(
#         Q(owner=active_business_user) |
#         Q(shared_permissions__shared_with=active_business_user,
#           shared_permissions__can_read=True)
#     ).distinct()

#     return render(request, 'your_template.html', {
#         'form': form,
#         'project_queryset': project_queryset
#     })