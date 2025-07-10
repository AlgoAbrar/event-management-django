from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Event, Category, RSVP
from .forms import EventForm, CategoryForm
from django.contrib.auth.models import Group


def get_user_role(user):
    if user.is_authenticated:
        if user.groups.filter(name='Admin').exists():
            return 'Admin'
        elif user.groups.filter(name='Organizer').exists():
            return 'Organizer'
        elif user.groups.filter(name='Participant').exists():
            return 'Participant'
    return None
# --- Role ---
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()


# --- Dashboard ---
@login_required
def dashboard_redirect(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_participant(request.user):
        return redirect('participant-dashboard')
    return redirect('event-list')


# --- Admin Dashboard ---
# @login_required
# @user_passes_test(is_admin)
# def admin_dashboard(request):
#     today = timezone.now().date()
#     context = {
#         'total_events': Event.objects.count(),
#         'total_participants': RSVP.objects.values('user').distinct().count(),
#         'upcoming_events_count': Event.objects.filter(date__gte=today).count(),
#         'past_events_count': Event.objects.filter(date__lt=today).count(),
#         'todays_events': Event.objects.filter(date=today),
#     }
#     return render(request, 'dashboard/admin_dashboard.html', context)
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    today = timezone.now().date()
    context = {
        'user_role': get_user_role(request.user),
        'total_events': Event.objects.count(),
        'total_participants': RSVP.objects.values('user').distinct().count(),
        'upcoming_events_count': Event.objects.filter(date__gte=today).count(),
        'past_events_count': Event.objects.filter(date__lt=today).count(),
        'todays_events': Event.objects.filter(date=today),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)



# --- Organizer Dashboard ---
# @login_required
# @user_passes_test(lambda u: is_organizer(u) or is_admin(u))
# def organizer_dashboard(request):
#     today = timezone.now().date()
#     event_type = request.GET.get('type', 'all')
#     events = Event.objects.select_related('category')

#     if event_type == 'upcoming':
#         events = events.filter(date__gte=today)
#     elif event_type == 'past':
#         events = events.filter(date__lt=today)
#     elif event_type == 'today':
#         events = events.filter(date=today)

#     context = {
#         'events': events,
#         'total_events': events.count(),
#         'upcoming_events_count': Event.objects.filter(date__gte=today).count(),
#         'past_events_count': Event.objects.filter(date__lt=today).count(),
#     }
#     return render(request, 'dashboard/organizer_dashboard.html', context)
@login_required
@user_passes_test(lambda u: is_organizer(u) or is_admin(u))
def organizer_dashboard(request):
    today = timezone.now().date()
    event_type = request.GET.get('type', 'all')
    events = Event.objects.select_related('category')

    if event_type == 'upcoming':
        events = events.filter(date__gte=today)
    elif event_type == 'past':
        events = events.filter(date__lt=today)
    elif event_type == 'today':
        events = events.filter(date=today)

    context = {
        'user_role': get_user_role(request.user),
        'events': events,
        'total_events': events.count(),
        'upcoming_events_count': Event.objects.filter(date__gte=today).count(),
        'past_events_count': Event.objects.filter(date__lt=today).count(),
    }
    return render(request, 'dashboard/organizer_dashboard.html', context)



# --- Participant Dashboard ---
# @login_required
# @user_passes_test(lambda u: is_participant(u) or is_admin(u))
# def participant_dashboard(request):
#     rsvp_events = Event.objects.filter(rsvps__user=request.user)
#     return render(request, 'dashboard/participant_dashboard.html', {'rsvp_events': rsvp_events})
@login_required
@user_passes_test(lambda u: is_participant(u) or is_admin(u))
def participant_dashboard(request):
    rsvp_events = Event.objects.filter(rsvps__user=request.user)
    context = {
        'user_role': get_user_role(request.user),
        'rsvp_events': rsvp_events,
    }
    return render(request, 'dashboard/participant_dashboard.html', context)



# --- Event List ---
@login_required
def event_list(request):
    search_query = request.GET.get('search', '')
    events = Event.objects.select_related('category')
    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )
    return render(request, 'events/show_events.html', {'events': events})


# --- RSVP Event ---
@login_required
@user_passes_test(lambda u: is_participant(u) or is_admin(u))
def rsvp_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('event-list')

    if RSVP.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, f"You have already RSVP’d to {event.name}.")
    else:
        RSVP.objects.create(user=request.user, event=event)
        messages.success(request, f"You have successfully RSVP’d to {event.name}.")
    return redirect('participant-dashboard')


# --- Category List ---
@login_required
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/show_category.html', {'categories': categories})


# --- Create Category ---
@login_required
@user_passes_test(is_admin)
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    return render(request, 'category/category_form.html', {'form': form})


# --- Update Category ---
@login_required
@user_passes_test(is_admin)
def category_update(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('category-list')

    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    return render(request, 'category/category_form.html', {'form': form})


# --- Delete Category ---
@login_required
@user_passes_test(is_admin)
def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        category.delete()
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
    return redirect('category-list')


# --- Create Event ---
@login_required
@user_passes_test(lambda u: is_organizer(u) or is_admin(u))
def event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('event-list')
    return render(request, 'events/events_form.html', {'form': form})


# --- Update Event ---
@login_required
@user_passes_test(lambda u: is_organizer(u) or is_admin(u))
def event_update(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('event-list')

    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event-list')
    return render(request, 'events/events_form.html', {'form': form})


# --- Delete Event ---
@login_required
@user_passes_test(is_admin)
def event_delete(request, pk):
    try:
        event = Event.objects.get(pk=pk)
        event.delete()
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
    return redirect('event-list')


# --- Event Detail ---
@login_required
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('event-list')

    rsvp_status = RSVP.objects.filter(user=request.user, event=event).exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'rsvp_status': rsvp_status
    })
