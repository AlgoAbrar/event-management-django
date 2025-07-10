from django import forms
import re
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group, Permission
from event.forms import StyledFormMixin

# Registration Form
class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        errors = []

        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            errors.append("Password must include at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            errors.append("Password must include at least one lowercase letter.")
        if not re.search(r"[0-9]", password):
            errors.append("Password must include at least one number.")
        if not re.search(r"[@#$%^&+=]", password):
            errors.append("Password must include at least one special character.")

        if errors:
            raise forms.ValidationError(errors)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False 
        if commit:
            user.save()
        return user

# Login 
class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Admin to assign roles
class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )

# Admin create group assign permission
class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permissions"
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
