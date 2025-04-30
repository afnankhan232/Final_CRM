# Basic Import
from django import forms

# ---- ==== Form for creating new Project ==== ----
from .models import Project

class ProjectCreationForm(forms.ModelForm):
        class Meta:
            # specifying the model we are targeting
            model = Project
            # Field to show in Form
            fields = ('name', 'description')

# ---- ==== Form for creating new Client ==== ----
from .models import Client

class ClientCreationForm(forms.ModelForm):
    class Meta:
        # specifying the model we are targeting
        model = Client
        # Field to show in Form
        fields = ('name', 'email', 'address', 'phone', 'description',)