from django.urls import path
from . import views

urlpatterns = [
    path('', views.organizer_dashboard, name='dashboard'),

    #Events
    path('events/', views.event_list, name='event-list'),
    path('events/create/', views.event_create, name='event-create'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),
    path('events/update/<int:pk>/', views.event_update, name='event-update'),
    path('events/delete/<int:pk>/', views.event_delete, name='event-delete'),

    #Participants
    path('participants/', views.participant_list, name='participant-list'),
    path('participants/create/', views.participant_create, name='participant-create'),
    path('participants/update/<int:pk>/', views.participant_update, name='participant-update'),
    path('participants/delete/<int:pk>/', views.participant_delete, name='participant-delete'),

    #Categories
    path('categories/', views.category_list, name='category-list'),
    path('categories/create/', views.category_create, name='category-create'),
    path('categories/update/<int:pk>/', views.category_update, name='category-update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category-delete'),
]
