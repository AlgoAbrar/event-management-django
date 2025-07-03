from django.shortcuts import render, redirect
from django.db.models import Count, Q
from datetime import date
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

def organizer_dashboard(request):
    type = request.GET.get('type', 'all')
    today = date.today()

    # Count values
    total_events = Event.objects.count()
    upcoming_events_count = Event.objects.filter(date__gte=today).count()
    past_events_count = Event.objects.filter(date__lt=today).count()
    total_participants = Participant.objects.count()
    todays_events = Event.objects.filter(date=today).select_related('category')

    base_query = Event.objects.select_related('category').prefetch_related('participants')

    if type == 'upcoming':
        events = base_query.filter(date__gte=today)
    elif type == 'past':
        events = base_query.filter(date__lt=today)
    elif type == 'today':
        events = base_query.filter(date=today)
    else:
        events = base_query.all()

    context = {
        'events': events,
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'todays_events': todays_events, 
    }

    return render(request, 'dashboard.html', context)

def event_list(request):
    search_query = request.GET.get('search', '')
    events = Event.objects.select_related('category').prefetch_related('participants')
    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))
    return render(request, 'show_events.html', {'events': events, 'search_query': search_query})

def participant_list(request):
    participants = Participant.objects.prefetch_related('events')
    return render(request, 'show_participants.html', {'participants': participants})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'show_category.html', {'categories': categories})

def event_create(request):
    form = EventForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('event-list')
    return render(request, 'events_form.html', {'form': form, 'title': 'Create Event'})

def participant_create(request):
    form = ParticipantForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('participant-list')
    return render(request, 'participants_form.html', {'form': form, 'title': 'Create Participant'})

def category_create(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    return render(request, 'category_form.html', {'form': form, 'title': 'Create Category'})

def event_update(request, pk):
    event = Event.objects.get(pk=pk)
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event-list')
    return render(request, 'events_form.html', {'form': form, 'title': 'Update Event'})

def participant_update(request, pk):
    participant = Participant.objects.get(pk=pk)
    form = ParticipantForm(request.POST, instance=participant)
    if form.is_valid():
        form.save()
        return redirect('participant-list')
    return render(request, 'participants_form.html', {'form': form, 'title': 'Update Participant'})

def category_update(request, pk):
    category = Category.objects.get(pk=pk)
    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category-list')
    return render(request, 'category_form.html', {'form': form, 'title': 'Update Category'})

def event_delete(request, pk):
    Event.objects.get(pk=pk).delete()
    return redirect('event-list')

def participant_delete(request, pk):
    Participant.objects.get(pk=pk).delete()
    return redirect('participant-list')

def category_delete(request, pk):
    Category.objects.get(pk=pk).delete()
    return redirect('category-list')

def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'show_events.html', {'event': event})