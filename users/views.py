from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserCreationForm, LoginForm, ProfileUpdateForm, PasswordChangeForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse


# ROLES
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()


# SIGN UP
def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()
            messages.success(request, 'Account created. Check your email to activate.')
            return redirect('sign-in')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# ACTIVATE ACCOUNT
def activate_user(request, user_id, token):
    try:
        user = CustomUser.objects.get(id=user_id)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated. Please log in.')
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid activation link.')

    except CustomUser.DoesNotExist:
        return HttpResponse('Activation failed. User not found.')

# SIGN IN
def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on role
            if is_admin(user):
                return redirect('admin-dashboard')
            elif is_organizer(user):
                return redirect('organizer-dashboard')
            elif is_participant(user):
                return redirect('user-dashboard')
            else:
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


# LOGOUT
@login_required
def sign_out(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('sign-in')


# PROFILE VIEW
@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


# EDIT PROFILE
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/update_profile.html', {'form': form})


# CHANGE PASSWORD
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data['old_password']):
                form.add_error('old_password', 'Incorrect current password')
            elif form.cleaned_data['new_password1'] != form.cleaned_data['new_password2']:
                form.add_error('new_password2', 'Passwords do not match')
            else:
                request.user.set_password(form.cleaned_data['new_password1'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully.')
                return redirect('profile')
    else:
        form = PasswordChangeForm()
    return render(request, 'accounts/password_change.html', {'form': form})


# ADMIN DASHBOARD
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/dashboard.html', {'users': users})


# CREATE GROUP
@login_required
@user_passes_test(is_admin)
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Group.objects.get_or_create(name=name)
            messages.success(request, f"Group '{name}' created.")
            return redirect('group-list')
    return render(request, 'admin/create_group.html')


# GROUP LIST
@login_required
@user_passes_test(is_admin)
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'admin/group_list.html', {'groups': groups})

# ASSIGN ROLE
@login_required
@user_passes_test(is_admin)
def assign_role(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    groups = Group.objects.all()

    if request.method == 'POST':
        group_name = request.POST.get('group')
        try:
            group = Group.objects.get(name=group_name)
            user.groups.clear()
            user.groups.add(group)
            messages.success(request, f"{user.username} is now a {group.name}.")
            return redirect('admin-dashboard')
        except Group.DoesNotExist:
            messages.error(request, f"Group '{group_name}' does not exist. Please create it first.")
            return redirect('create-group')  # or redirect back to assign-role if you prefer

    return render(request, 'admin/assign_role.html', {'user_obj': user, 'groups': groups})

@login_required
@user_passes_test(is_admin)
@require_POST
def delete_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        if group.name == 'Admin':
            messages.error(request, "Cannot delete the Admin group.")
        else:
            group.delete()
            messages.success(request, f"Group '{group.name}' deleted.")
    except Group.DoesNotExist:
        messages.error(request, "Group not found.")
    return redirect('group-list')