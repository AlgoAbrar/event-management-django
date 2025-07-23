from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Event, Category, RSVP
from .forms import EventForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
# Role Helpers
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_user(user):
    return user.groups.filter(name='User').exists()

# Event List for Everyone
def show_events(request):
    events = Event.objects.select_related('category').prefetch_related('rsvps')
    return render(request, 'event/show_event.html', {'events': events})


# # Event Details & RSVP
# @login_required
# def event_detail(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     has_rsvped = RSVP.objects.filter(user=request.user, event=event).exists()

#     if request.method == 'POST' and not has_rsvped:
#         RSVP.objects.create(user=request.user, event=event)
#         messages.success(request, 'You have RSVP’d successfully.')
#         return redirect('event-detail', event_id=event.id)

#     return render(request, 'event/event_details.html', {
#         'event': event,
#         'has_rsvped': has_rsvped
#     })
class EventDetailView(LoginRequiredMixin, View):
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        has_rsvped = RSVP.objects.filter(user=request.user, event=event).exists()
        return render(request, 'event/event_details.html', {
            'event': event,
            'has_rsvped': has_rsvped
        })

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        has_rsvped = RSVP.objects.filter(user=request.user, event=event).exists()
        if not has_rsvped:
            RSVP.objects.create(user=request.user, event=event)
            messages.success(request, 'You have RSVP’d successfully.')
        return redirect('event-detail', event_id=event.id)


# # Create Event
# @login_required
# @user_passes_test(lambda u: is_organizer(u) or is_admin(u))
# def create_event(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Event created successfully.')
#             return redirect('show-events')
#     else:
#         form = EventForm()
#     return render(request, 'event/event_form.html', {'form': form})

class CreateEventView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    
    def test_func(self):
        return is_organizer(self.request.user) or is_admin(self.request.user)
    
    def get_success_url(self):
        messages.success(self.request, 'Event created successfully.')
        return reverse_lazy('show-events')


# Organizer Dashboard
@login_required
@user_passes_test(is_organizer)
def organizer_dashboard(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'event/dashboard/manager-dashboard.html', {'events': events})


# Participant Dashboard
@login_required
@user_passes_test(is_user)
def user_dashboard(request):
    rsvp_events = request.user.rsvp_events.all()
    return render(request, 'event/dashboard/user-dashboard.html', {'events': rsvp_events})

# @login_required
# @user_passes_test(is_organizer)
# def participants_list(request):
#     rsvps = RSVP.objects.select_related('user', 'event').all()
#     return render(request, 'event/participants_list.html', {'rsvps': rsvps})
class ParticipantsListView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return is_organizer(self.request.user)

    def get(self, request):
        rsvps = RSVP.objects.select_related('user', 'event').all()
        return render(request, 'event/participants_list.html', {'rsvps': rsvps})


# @login_required
# @user_passes_test(lambda u: is_organizer(u) or is_admin(u))
# def edit_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)

#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES, instance=event)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Event updated successfully.')
#             return redirect('organizer-dashboard')
#     else:
#         form = EventForm(instance=event)

#     return render(request, 'event/event_form.html', {'form': form, 'edit': True})
class EditEventView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    context_object_name = 'event'

    def test_func(self):
        return is_organizer(self.request.user) or is_admin(self.request.user)

    def get_success_url(self):
        messages.success(self.request, 'Event updated successfully.')
        return reverse_lazy('organizer-dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        return context


# # Delete event
# @login_required
# @user_passes_test(lambda u: is_organizer(u) or is_admin(u))
# def delete_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)

#     if request.method == 'POST':
#         event.delete()
#         messages.success(request, 'Event deleted successfully.')
#         return redirect('organizer-dashboard')

#     # Confirmation page
#     return render(request, 'event/event_confirm_delete.html', {'event': event})
class DeleteEventView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return is_organizer(self.request.user) or is_admin(self.request.user)

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        return render(request, 'event/event_confirm_delete.html', {'event': event})

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('organizer-dashboard')