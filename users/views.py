from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.contrib import messages
from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm, LoginForm

# Role
def get_user_role(user):
    if user.is_authenticated:
        if user.groups.filter(name='Admin').exists():
            return 'Admin'
        elif user.groups.filter(name='Organizer').exists():
            return 'Organizer'
        elif user.groups.filter(name='Participant').exists():
            return 'Participant'
    return None

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

# Signup view
def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False 
            user.save()
            messages.success(request, 'A confirmation email has been sent. Please check your inbox to activate your account.')
            return redirect('sign-in')
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'registration/register.html', {"form": form})

# Login view
def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, 'Your account is not activated. Please check your email.')
                return redirect('sign-in')
            login(request, user)

            
            if is_admin(user):
                return redirect('admin-dashboard')
            elif is_organizer(user):
                return redirect('organizer-dashboard')  
            elif is_participant(user):
                return redirect('participant-dashboard')  
            else:
                return redirect('home')
    return render(request, 'registration/login.html', {'form': form})

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    
    return render(request, 'registration/logout.html')

# Account activation
# def activate_user(request, user_id, token):
#     try:
#         user = User.objects.get(id=user_id)
#         if default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             messages.success(request, 'Your account has been activated successfully. You can now log in.')
#             return redirect('sign-in')
#         else:
#             return HttpResponse('Invalid activation link or token.', status=400)
#     except User.DoesNotExist:
#         return HttpResponse('User not found.', status=404)

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')

# Admin dashboard
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    for user in users:
        user.group_name = user.all_groups[0].name if user.all_groups else 'No Group Assigned'

    return render(request, 'admin/dashboard.html', {"users": users})

# Admin assign roles
@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned the role '{role.name}'.")
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form, "user": user})

# Admin create groups roles
@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' has been created successfully.")
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {'form': form})

# Admin view
@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})
