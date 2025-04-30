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
        

        def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)  # fallback to None
            super().__init__(*args, **kwargs)
        
        # Since we need the name of the each form to be unique for a user
        # we need to over-ride the [clean] method
        # It prevent from unusual error page
        def clean_name(self):
            name = self.cleaned_data.get('name')
            if Project.objects.filter(name=name, user=self.user).exists():
                raise forms.ValidationError("You already have a project with this name.")
            return name


# ---- ==== Form for creating new Client ==== ----
from .models import Client

class ClientCreationForm(forms.ModelForm):
    class Meta:
        # specifying the model we are targeting
        model = Client
        # Field to show in Form
        fields = ('name', 'email', 'address', 'phone', 'description',)