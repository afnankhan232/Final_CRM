# Basic Import
from django import forms

# no active use
# For Displaying [country_code] and [phone_number] side-by-side
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Fieldset, Div
from accounts.models import AccessPermission
from accounts.models import BusinessUser

# ---- ==== Form for CREATING new Project / UPDATING existing Project ==== ----
from .models import Project

class ProjectCreationForm(forms.ModelForm):
    class Meta:
        # specifying the model we are targeting
        model = Project
        # Field to show in Form
        fields = ('name', 'description')
    

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # fallback to None
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter the list name'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Enter a description for the list'
        })
    
    # Since we need the name of the each form to be unique for a user
    # we need to over-ride the [clean] method
    # It prevent from unusual error page
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Project.objects.filter(name=name, user=self.user).exists():
            raise forms.ValidationError("You already have a project with this name.")
        return name


# ---- ==== Form for CREATING new Client OR UPDATING existing Client ==== ----
from .models import Client

class ClientCreationForm(forms.ModelForm):
    class Meta:
        # specifying the model we are targeting
        model = Client
        # Field to show in Form
        fields = ('name', 'email', 'country_code', 'phone', 'address', 'description', 'list')

    # We need to over-ride the __init__ method (getting the projects from current user)
    # we also include the 'user' field in the views.py
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        try:
            possible_projects = kwargs.pop('possible_projects', None)
        except:
            possible_projects = None

        # Don't  mess with the original __init__ method! EVER
        super().__init__(*args, **kwargs)

        # The following code set the possible value of project
        if user:
            if possible_projects != None:
                self.fields['list'].queryset = possible_projects
            else:
                self.fields['list'].queryset = Project.objects.filter(user = user)
        
        # Making ['email' and 'phone'] fields optional - for crispy form
        self.fields['email'].required = False
        self.fields['phone'].required = False

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter name'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter email'
        })
        self.fields['phone'].widget.attrs.update({
            'placeholder': 'Enter phone number'
        })
        self.fields['address'].widget.attrs.update({
            'placeholder': 'Enter location'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Add a description'
        })
        self.fields['list'].empty_label = 'Select list'


# ---- ==== Form for creating new documents ==== ----
from .models import Document

class DocumentCreationForm(forms.ModelForm):
    class Meta:

        # specifying the model we are targeting
        model = Document

        # Field to show in Form
        fields = ('document_name', 'file', 'related_to', 'description')
    

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # fallback to None
        super().__init__(*args, **kwargs)

        # The following code set the possible value of document
        if self.user:
            self.fields['related_to'].queryset = Client.objects.filter(companyAssignee = self.user)
        self.fields['document_name'].widget.attrs.update({
            'placeholder': 'Enter document name'
        })
        self.fields['related_to'].empty_label = 'Select contact'
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Add a description'
        })
        


# ---- ==== ProjectAccessForm ==== ----
from .models import ProjectAccessPermission
from client.models import Project

class ProjectAccessPermissionForm_Client(forms.ModelForm):
    project_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    project_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = ProjectAccessPermission
        fields = [
            'project_name',
            'can_read_project',
            'can_edit_project',
            'can_delete_project',
            'can_permanent_delete_project',
        ]
        widgets = {
            'project_name': forms.Select(attrs={'class': 'form-select'}),
            'can_read_project': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_edit_project': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_delete_project': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_permanent_delete_project': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# ---- ==== Task Creation Form ==== ----
from .models import Task
class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'task_name',
            'description',
            'status',
            'priority',
            'owner',
            'type',
            'related_to',
            # 'due_date',
            # 'due_time',
        ]
    # We have to improve it based on current account!

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            print(Client.objects.filter(companyAssignee = user))
            self.fields['related_to'].queryset = Client.objects.filter(companyAssignee = user)
            self.fields['owner'].queryset = BusinessUser.objects.filter(pk = user.pk)
        
        self.fields['task_name'].widget.attrs.update({
            'placeholder': 'Enter task name'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Enter task description'
        })
        self.fields['related_to'].empty_label = 'Select a contact'


#Task Edit Form

class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'task_name',
            'description',
            'status',
            'priority',
            'owner',
            'type',
            'related_to',
            'due_date',
            'due_time',
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    # We have to improve it based on current account!

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            print(Client.objects.filter(companyAssignee = user))
            self.fields['related_to'].queryset = Client.objects.filter(companyAssignee = user)
            self.fields['owner'].queryset = BusinessUser.objects.filter(pk = user.pk)
        
        self.fields['task_name'].widget.attrs.update({
            'placeholder': 'Enter task name'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Enter task description'
        })
        self.fields['related_to'].empty_label = 'Select a contact'