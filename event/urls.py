from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard_redirect, name='dashboard-redirect'),

    # Dashboards
    path('dashboard/admin/', views.admin_dashboard, name='admin-dashboard'),
    path('dashboard/organizer/', views.organizer_dashboard, name='organizer-dashboard'),
    path('dashboard/participant/', views.participant_dashboard, name='participant-dashboard'),

    # Events
    path('', views.event_list, name='event-list'),
    path('event/<int:pk>/', views.event_detail, name='event-detail'),
    path('event/create/', views.event_create, name='event-create'),
    path('event/<int:pk>/update/', views.event_update, name='event-update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event-delete'),

    path('event/<int:event_id>/rsvp/', views.rsvp_event, name='event-rsvp'),

    # Categories
    path('categories/', views.category_list, name='category-list'),
    path('categories/create/', views.category_create, name='category-create'),
    path('categories/<int:pk>/update/', views.category_update, name='category-update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),
]
