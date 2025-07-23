from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from users.views import sign_up, sign_in, sign_out, activate_user, profile, edit_profile, change_password, admin_dashboard,create_group, assign_role, group_list, delete_group


urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),

    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'),
    

    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit-profile'),
    path('password/change/', change_password, name='password-change'),

    # Password Reset URLs
    path('password/reset/', PasswordResetView.as_view(
        template_name='registration/reset_email.html',
        success_url='/users/sign-in/'
    ), name='password-reset'),

    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/reset_password.html',
        success_url='/users/sign-in/'
    ), name='password-reset-confirm'),

    # Admin URLs
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/assign-role/<int:user_id>/', assign_role, name='assign-role'),
    path('admin/group-list/', group_list, name='group-list'),
    path('groups/delete/<int:group_id>/', delete_group, name='delete-group'),
]
