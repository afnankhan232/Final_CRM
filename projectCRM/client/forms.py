# Basic Import
from django import forms

# For Displaying [country_code] and [phone_number] side-by-side
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Fieldset, Div

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
        fields = ('name', 'email', 'country_code', 'phone', 'address', 'description', 'list')

    # We need to over-ride the __init__ method (getting the projects from current user)
    # we also include the 'user' field in the views.py
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        # Don't  mess with the original __init__ method! EVER
        super().__init__(*args, **kwargs)

        # The following code set the possible value of project
        if user:
            self.fields['list'].queryset = Project.objects.filter(user = user)
        
        # Making ['email' and 'phone'] fields optional - for crispy form
        self.fields['email'].required = False
        self.fields['phone'].required = False
        
        # Chaning the Layout of side-by-side display for [country_code] and [phone_number]
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name'),
            Field('email'),
            Div(
                Div('country_code', css_class='pr-2', style='flex: 1;'),
                Div('phone', style='flex: 3;'),
                css_class='d-flex align-item-end'
            ),
            Field('address'),
            Field('description'),
            Field('list'),
        )
