# ---- ==== Import Statement Goes HERE ==== ----
# Basic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

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

# from client
from client.models import ProjectAccessPermission
from client.forms import TaskCreationForm

# Date Time Field
from django.utils import timezone

from accounts.models import Role

# MORE SECURITY
def get_active_business_user_with_permission(request, permission_field_name: str, show_err = None, fallback = False):
    """
    ASK: do I have a permission?
    Verifies if the logged-in user has the required permission on the active business account.
    
    Args:
        request: The HTTP request object.
        permission_field_name: A string name of the permission field (e.g. "can_read_project").
        show_err:
        fallBack: 
    Returns:
        BusinessUser: the active_business_user object.

    Raises:
        PermissionDenied: if permission is not granted or not found.
        Success: Boolean Value
    """

    logged_in_user = request.user.businessuser
    active_id = request.session.get('active_business_user_id')

    if(active_id == None):
        request.session['active_business_user_id'] = request.user.businessuser.id
        messages.warning(request, "Something Went Wrong - Reverting to own account.")

    active_business_user = get_object_or_404(BusinessUser, id=active_id)

    if logged_in_user == active_business_user:
        return (active_business_user, True)

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

    if request.session.get('active_business_user_id') == None:
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

    if request.session.get('active_business_user_id') == None:
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

@require_POST
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
                if get_active_business_user_with_permission(request, 'can_add_project', show_err='Add')[1] == True:
                    projectValidForm = formA.save(commit = False)
                    projectValidForm.user = active_business_user
                    projectValidForm.save() # Save the form
                    messages.success(request, f"New Project Created Successfully!")
            else:
                messages.error(request, "Project Name should be unique!")
            return redirect('appContacts')
        
        elif(form_type == 'client_form'):
            formA = ProjectCreationForm(user = user)
            # the user arguement pass to the __init__ attribute of the ProjectCreationForm (it's no big deal)
            formB = ClientCreationForm(request.POST, user = user)

            if(formB.is_valid()):
                if get_active_business_user_with_permission(request, 'can_add_contact', show_err='Add')[1] == True:
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
        print("I am here!!")
        # projects = Project.objects.filter(
        #     shared_project_permissions__shared_with = logged_in_user,
        #     shared_project_permissions__can_read_project = True,
        #     user = active_business_user,
        # )
        # Get all roles that the active user shared with the logged-in user
        shared_roles = AccessPermission.objects.filter(
            owner=active_business_user,
            shared_with=logged_in_user
        ).values_list('role', flat=True)

        # Get all projects using those shared roles with read access
        projects = Project.objects.filter(
            shared_project_permissions__role__in=shared_roles,
            shared_project_permissions__can_read_project=True,
            user=active_business_user
        ).distinct()

        contacts = Client.objects.filter(
            list__in = projects,
            companyAssignee=active_business_user,
        )

    project_name = request.GET.get('project_name')
    if project_name:
        contacts = contacts.filter(list__name = project_name)
    
    context = {
        'formA': formA,
        'formB': formB,
        'contacts': contacts,
        'projects': projects,
        'total_contacts': contacts.count(),
        'selected_project_name': project_name,
        'set_to_all': True if project_name is None else False,
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
        documents = Document.objects.filter(user = logged_in_user, related_to=contact)

    elif is_success == True:
        # Get all roles that the active user shared with the logged-in user
        shared_roles = AccessPermission.objects.filter(
            owner=active_business_user,
            shared_with=logged_in_user
        ).values_list('role', flat=True)

        # Get all projects using those shared roles with read access
        projects = Project.objects.filter(
            shared_project_permissions__role__in=shared_roles,
            shared_project_permissions__can_read_project=True,
            user=active_business_user
        ).distinct()

        contact = get_object_or_404(
            Client,
            list__in = projects,
            companyAssignee=active_business_user,
            pk=pk,
        )

        if get_active_business_user_with_permission(request, 'can_read_document', show_err='Contact Read')[1]:
            documents = Document.objects.filter(user = logged_in_user, related_to=contact)
        else:
            documents = None
    else:
        return redirect('appContacts')
    
    form_type = request.POST.get("form_type")
    # Client Updation Form
    if(request.method == "POST"):
        if(form_type != None):
            formEditClient = ClientCreationForm(request.POST, user = active_business_user, possible_projects = projects, instance = contact)
            if(formEditClient.is_valid()):
                if get_active_business_user_with_permission(request, 'can_edit_contact', show_err='Client Edit')[1] == True:
                    formEditClient.last_edit = timezone.now()
                    formEditClient.save()
                    messages.success(request, "Client information Updated!")
            else:
                messages.error(request, "Can't edit the user detail!")
        return redirect('appContactDetail', pk=pk)
    
    formEditClient = ClientCreationForm(user = active_business_user, possible_projects = projects, instance = contact)
    context = {
        'contact': contact,
        'form': formEditClient,
        'documents': documents,
        'businessuser': user,
    }
    return render(
        request,
        'featuredApp/contact_detailed.html',
        context,
    )

@require_POST
@login_required
def contact_delete_view(request, pk):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_delete_contact', show_err='Delete')

    if(is_success == False):
        return redirect('appContactDetail', pk=pk)
    
    contact = get_object_or_404(Client, companyAssignee = active_business_user, pk=pk)
    contact_name = contact.name
    contact.soft_delete()
    messages.warning(request, f"Client '{contact_name}' is deleted!")

    return redirect('appContacts')

@require_POST
@login_required
def contact_permanent_delete_view(request, pk):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_permanent_delete_contact', show_err='Permanent Delete')

    if(is_success == False):
        return redirect('appTrash')
    
    contact = get_object_or_404(Client.all_objects, companyAssignee = active_business_user, pk=pk)
    contact_name = contact.name
    contact.delete()
    messages.warning(request, f"Client '{contact_name}' is deleted permanently!")
    return redirect('appTrash')

@require_POST
@login_required
def contact_restore_view(request, pk):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_delete_contact', show_err='Restore')

    if(is_success == False):
        return redirect('appTrash')

    contact = get_object_or_404(Client.all_objects, companyAssignee = active_business_user, pk=pk)
    contact_name = contact.name
    contact.restore()
    messages.success(request, f"Restored Contact '{contact_name}")
    return redirect('appTrash')

@require_POST
@login_required
def project_delete_view(request, name, *args, **kwargs):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser

    active_id = request.session['active_business_user_id']
    if(active_id == None):
        request.session['active_business_user_id'] = request.user.businessuser.id

    active_business_user = get_object_or_404(BusinessUser, id=active_id)
    
    project = get_object_or_404(Project, user=active_business_user, name=name)
    project_name = project.name

    if project_name == "Default" :
        messages.warning(request, "Default Project can't be deleted")
        url = reverse('appContacts')
        redirect_url = f"{url}?project_name={name}"
        return redirect(redirect_url)
    
    messages.warning(request, f"Project '{project_name}' is deleted.")
    project.soft_delete()
    return redirect('appContacts')

@require_POST
@login_required
def project_restore_view(request, id, *args, **kwargs):

    project = Project.all_objects.filter(id = id).first()
    project_name = project.name

    project.restore()
    messages.success(request, f"Project {project_name} is recovered.")

    return redirect('appTrash')

# ---- ==== Featured Related to Tasks View ==== ----
# Include: [tasks_view; ]
@login_required
def tasks_view(request, *args, **kwargs):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    form = TaskCreationForm()

    context = {
        'form': form,
        'businessuser': user,
    }
    return render(
        request, 
        'featuredApp/tasks.html',
        context,
    )

# ---- ==== Featured Related to Documents View ==== ----
# Include: [document_view; ]
@login_required
def documents_view(request, *args, **kwargs):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_read_documents', show_err='Document Read')

    if request.method == "POST":
        # For the purpose of file upload - we need request.FILES [COOL]
        form = DocumentCreationForm(request.POST, request.FILES, user = user)

        if(form.is_valid()):
            if(get_active_business_user_with_permission(request, 'can_edit_documents', show_err='Document Edit')[1]):
                tmp = form.save(commit = False)
                tmp.user = user
                tmp.save()
                messages.success(request, f"New Document Added!")
        else:
            messages.success(request, f"Can't Create Document")
        return redirect('appDocuments')
    else:
        form = DocumentCreationForm(user = user)

    if(is_success == False):
        documents = None
    
    elif(logged_in_user != active_business_user):
        # Get all roles that the active user shared with the logged-in user
        shared_roles = AccessPermission.objects.filter(
            owner=active_business_user,
            shared_with=logged_in_user
        ).values_list('role', flat=True)

        # Get all projects using those shared roles with read access
        projects = Project.objects.filter(
            shared_project_permissions__role__in=shared_roles,
            shared_project_permissions__can_read_project=True,
            user=active_business_user
        ).distinct()

        # Get All Client Associated with in these projects
        clients = Client.objects.filter(list__in=projects)

        # Get All Document these Client have
        documents = Document.objects.filter(related_to__in=clients)

    else:
        documents = Document.objects.filter(user=user)

    return render(
        request, 
        'featuredApp/documents.html',
        {
            "documents": documents,
            'total_documents': documents.count() if documents != None else 0, 
            "form": form,
            'businessuser': user,
        }
    )

@login_required
def documents_detailed_view(request, pk, *args, **kwargs):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_read_documents', show_err='Document Read')
    document = get_object_or_404(Document, user=active_business_user, pk=pk)
    form_type = request.POST.get("form_type")

    if(request.method == "POST"):
        if(form_type!=None):
            formEditDocument = DocumentCreationForm(request.POST, user = active_business_user, instance = document)
            if(formEditDocument.is_valid()):
                if get_active_business_user_with_permission(request, 'can_edit_document', show_err='Document Edit')[1] == True:
                    formEditDocument.save()
                    messages.success(request, "Document Updated!")
            else:
                messages.error(request, "Can't Edit Document!")
        return redirect('appDocumentDetail', pk=pk)
    
    formEditDocument = DocumentCreationForm(user = active_business_user, instance = document)
    context = {
        'document': document,
        'form': formEditDocument,
        'businessuser': user,
    }
    return render(
        request,
        'featuredApp/documents_detailed.html',
        context,
    )

@require_POST
@login_required
def document_delete_view(request, pk):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_delete_documents', show_err='Document Delete')

    if(is_success == False):
        return redirect('appDocumentDetail', pk=pk)

    document = get_object_or_404(Document, user = active_business_user, pk=pk)
    document_name = document.document_name
    document.soft_delete()
    messages.warning(request, f"Document '{document_name}' is deleted!")
    return redirect('appDocuments')

@require_POST
@login_required
def document_permanent_delete_view(request, pk):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_permanent_delete_contact', show_err='Permanent Delete')

    if(is_success == False):
        return redirect('appTrash')

    document = get_object_or_404(Document.all_objects, user = active_business_user, pk=pk)
    document_name = document.document_name
    document.delete()
    messages.warning(request, f"Document '{document_name}' is deleted permanently!")
    return redirect('appTrash')

@require_POST
@login_required
def document_restore_view(request, pk):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_business_user, is_success = get_active_business_user_with_permission(request, 'can_delete_document', show_err='Restore')

    if(is_success == False):
        return redirect('appTrash')

    document = get_object_or_404(Document.all_objects, user = active_business_user, pk=pk)
    document_name = document.document_name
    document.restore()
    messages.success(request, f"Restored Document '{document_name}")
    return redirect('appTrash')

# ---- ==== Featured Related to Activities View ==== ----
# Include: [activities_view; ]
@login_required
def activities_view(request, *args, **kwargs):
    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    context = {
        'businessuser': user,
    }
    return render(
        request, 
        'featuredApp/activities.html',
        context,
    )

# ---- ==== Featured Related to Trash View ==== ----
# Include: [trash_view; ]
@login_required
def trash_view(request):

    user = request.user.businessuser
    logged_in_user = request.user.businessuser
    active_id = request.session.get('active_business_user_id')
    active_business_user = get_object_or_404(BusinessUser, id=active_id)

    if(logged_in_user != active_business_user):
        if(get_active_business_user_with_permission(request, 'can_delete_contact', show_err='Contact Delete')[1]):
            trashed_contacts = Client.all_objects.filter(companyAssignee = active_business_user, is_deleted = True)
        
        # Get all roles that the active user shared with the logged-in user
        shared_roles = AccessPermission.objects.filter(
            owner=active_business_user,
            shared_with=logged_in_user
        ).values_list('role', flat=True)

        # Get all projects using those shared roles with delete(restore) access
        projects = Project.objects.filter(
            shared_project_permissions__role__in=shared_roles,
            shared_project_permissions__can_delete_project=True,
            user=active_business_user
        ).distinct()

        if(get_active_business_user_with_permission(request, 'can_delete_documents', show_err='Document Delete')[1]):
            trashed_documents = Document.all_objects.filter(user = active_business_user, is_deleted = True)
    else:
        trashed_contacts = Client.all_objects.filter(companyAssignee=user, is_deleted=True)
        trashed_projects = Project.all_objects.filter(user=user, is_deleted=True)
        trashed_documents = Document.all_objects.filter(user=user, is_deleted=True)

    print(trashed_projects)
    context = {
        'trashed_contacts': trashed_contacts,
        'trashed_documents': trashed_documents,
        'trashed_projects': trashed_projects,
        'businessuser': user,
    }

    return render(
        request,
        'featuredApp/trash.html',
        context,
    )

# ---- ==== Manage User Access ==== ----
from accounts.forms import RolesCreationForm_Account
from client.forms import ProjectAccessPermissionForm_Client
from accounts.models import AccessPermission
from django.forms import modelformset_factory
# This funciton is valid up to the logged in user!
# And take about 3 days of debug to create!
# And 'Roles' form can use some better design!
@login_required
def manage_access(request):
    user = request.user.businessuser
    projects = Project.objects.filter(user=user)
    roles = Role.objects.filter(user=user)
    accesses = AccessPermission.objects.filter(owner=user)

    # Forms
    role_form = RolesCreationForm_Account(user=user)
    permission_formset_factory = modelformset_factory(
        ProjectAccessPermission,
        form=ProjectAccessPermissionForm_Client,
        extra=len(projects)
    )
    permission_formset = None

    if request.method == "POST":
        role_form = RolesCreationForm_Account(request.POST, user=user)
        permission_formset = permission_formset_factory(request.POST, queryset=ProjectAccessPermission.objects.none())
        form_type = request.POST.get("form_type")

        if form_type == 'role_form':
            if role_form.is_valid() and permission_formset.is_valid():
                try:
                    role_instance = role_form.save(commit=False)
                    role_instance.user = user
                    role_instance.save()

                    for form, project in zip(permission_formset, projects):
                        permission_instance = form.save(commit=False)
                        permission_instance.project = project
                        permission_instance.role = role_instance
                        permission_instance.save()

                    messages.success(request, f"The role '{role_instance.name}' has been created successfully.")
                    return redirect('appManageAccess')

                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
            elif(role_form.is_valid() == False):
                messages.error(request, f"Role With Same Name Already Exist")
            else:
                messages.error(request, "Please correct the errors in the form.")
            return redirect('appManageAccess')
        elif form_type == "access_form":
            emails = request.POST.getlist('shared_with_emails')
            roles_ids = request.POST.getlist('roles')
            success = True
            for email, role_id in zip(emails, roles_ids):
                try:
                    shared_user = BusinessUser.objects.get(company_email=email)
                    role = Role.objects.get(id=role_id, user=user)
                    AccessPermission.objects.create(
                        owner=user,
                        shared_with=shared_user,
                        role=role,
                    )
                except BusinessUser.DoesNotExist:
                    messages.error(request, f"User with email {email} does not exist.")
                    success = False
                except Role.DoesNotExist:
                    messages.error(request, f"Invalid role selected.")
                    success = False
                except Exception as e:
                    messages.error(request, f"Error sharing access with {email}: {str(e)}")
                    success = False

            if success:
                messages.success(request, "Access shared successfully.")
            return redirect('appManageAccess')

    # GET request - prepare empty formset with initial values
    initial_data = [{
        'project_id': project.id,
        'project_name': project.name,
        'can_read_project': False,
        'can_edit_project': False,
        'can_delete_project': False,
        'can_permanent_delete_project': False,
    } for project in projects]

    permission_formset = permission_formset_factory(
        queryset=ProjectAccessPermission.objects.none(),
        initial=initial_data,
    )

    # Pair forms with corresponding projects
    formset_with_projects = zip(permission_formset, projects)

    context = {
        'formA': role_form,
        'formB': permission_formset,
        'formB_with_project_queryset': formset_with_projects,
        'project_queryset': projects,
        'roles': roles,
        'accesses': accesses,
        'businessuser': user,
    }
    return render(request, 'featuredApp/manage_access.html', context)

@require_POST
@login_required
def delete_role(request, role_id):
    role = get_object_or_404(Role, id=role_id, user=request.user.businessuser)
    role_name = role.name
    role.delete()
    messages.warning(request, f"Role '{role_name}' deleted.")
    return redirect('appManageAccess')

@require_POST
@login_required
def delete_access(request, access_id):
    access = get_object_or_404(AccessPermission, id=access_id, owner=request.user.businessuser)
    shared_with = access.shared_with  # Access for feedback
    access.delete()
    messages.warning(request, f"Access revoked for {shared_with.company_email}.")
    return redirect('appManageAccess')