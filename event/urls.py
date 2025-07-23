from django.urls import path
from .views import show_events, event_detail, create_event,organizer_dashboard, user_dashboard, participants_list
from .views import EventDetailView,DeleteEventView,EditEventView,ParticipantsListView,CreateEventView
from .views import edit_event, delete_event

urlpatterns = [
    path('', show_events, name='show-events'),
    # path('event/<int:event_id>/', event_detail, name='event-detail'),
    path('event/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    #path('create/', create_event, name='create-event'),
    path('event/create/', CreateEventView.as_view(), name='create-event'),
    path('organizer/dashboard/', organizer_dashboard, name='organizer-dashboard'),
    path('user/dashboard/', user_dashboard, name='user-dashboard'),
    #path('participants/', participants_list, name='participants-list'),
    path('participants/', ParticipantsListView.as_view(), name='participants-list'),
    # path('event/<int:event_id>/edit/', edit_event, name='edit-event'),
    path('event/<int:pk>/edit/', EditEventView.as_view(), name='edit-event'),
    # path('event/<int:event_id>/delete/', delete_event, name='delete-event'),
    path('event/<int:event_id>/delete/', DeleteEventView.as_view(), name='delete-event'),
    
]
