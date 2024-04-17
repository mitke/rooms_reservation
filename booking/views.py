from django.shortcuts import render, redirect, get_object_or_404
from .models import Rooms, Bookings
from .forms import BookingForm, RegistrationForm
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


def home(request):
  current_time = timezone.now()
  #print(current_time)
  print(timezone.now() + timezone.timedelta(days=14))
  rooms = Rooms.objects.all()
  room_availability = {}

  for soba in rooms:
    upcoming_bookings = Bookings.objects.filter(room=soba, start_time__gte=current_time, start_time__lt=current_time + timezone.timedelta(days=7)).order_by('start_time') # samo 14 dana unapred
    #upcoming_bookings = Bookings.objects.filter(room=soba, start_time__gte=current_time, end_time__gte=current_time).order_by('start_time')
    room_availability[soba] = upcoming_bookings
  return render(request, 'booking/home.html', {'rooms': rooms, 'room_availability': room_availability})


def user_logout(request):
  logout(request)
  return redirect('home')


def user_login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('home')
  else:
    form = AuthenticationForm()
  return render(request, 'register/login.html', {'form': form})


def user_register(request):
  if request.method == 'POST':
    user_form = RegistrationForm(request.POST)
    
    if user_form.is_valid():
      user = user_form.save()
      login(request, user)
      return redirect('home')
      
  else:
    user_form = RegistrationForm()
    
  return render(request, 'register/register.html', {'user_form': user_form})   

      
@login_required
def room_list(request):
  current_time = timezone.now()
  rooms = Rooms.objects.all()
  room_availability = {}

  for soba in rooms:
    upcoming_bookings = Bookings.objects.filter(room=soba, start_time__gte=current_time).order_by('start_time')
    room_availability[soba] = upcoming_bookings
  return render(request, 'booking/room_list.html', {'rooms': rooms, 'room_availability': room_availability})


@login_required
def book_room(request, room_id):
  soba = Rooms.objects.get(pk=room_id)
  soba_capacity = soba.capacity
  soba_projector = soba.projector
  current_time = timezone.now()

  if request.method == 'POST':
    form = BookingForm(request.POST)
    if form.is_valid():

      start_time = request.POST.get('start_time')
      start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
      start_time_aware = timezone.make_aware(start_time, timezone.get_default_timezone())
      end_time = request.POST.get('end_time')
      end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
      end_time_aware = timezone.make_aware(end_time, timezone.get_default_timezone())
      try:
        expected_participants = int(request.POST.get('expected_participants'))
      except ValueError:
        expected_participants = 0
      needs_projector = request.POST.get('needs_projector')
      
      message = provera(start_time_aware, end_time_aware, current_time, expected_participants, soba_capacity, soba_projector, needs_projector, room_id, None)

      if message != None:
        messages.error(request, message)
        return render(request, 'booking/book_room.html', {'room': soba, 'form': form})
      else:
        booking = form.save(commit=False)
        booking.room = soba
        booking.user = request.user
        booking.save()
        messages.success(request, 'Prostorija je uspoešno rezervisana')
        #return redirect('home')                          # ovo vraća uvek na vrh
        redirect_url = reverse('home') + '#' + str(room_id)   # ova dva reda 
        return HttpResponseRedirect(redirect_url)             # vraćaju na anchor tag
    
  else:
    form = BookingForm()  

  return render(request, 'booking/book_room.html', {'room': soba, 'form': form})


@login_required
def delete_booking(request, booking_id):
  booking = get_object_or_404(Bookings, pk=booking_id)
  
  #if request.user == booking.user:
  booking.delete()
  #else:
    #messages.error(request, 'You do not have permission to edit this reservation.')
  #return redirect('home')
  redirect_url = reverse('home') + '#' + str(room_id)
  return HttpResponseRedirect(redirect_url)


@login_required
def edit_booking(request, booking_id):
  booking = get_object_or_404(Bookings, pk=booking_id)
  room_name = booking.room.name
  room_id = booking.room
  soba_capacity = booking.room.capacity
  soba_projector = booking.room.projector
  edit_mode = True
  current_time = timezone.now()

  if request.method == 'POST':
    form = BookingForm(request.POST, instance=booking)
    
    if form.is_valid():
      start_time = request.POST.get('start_time')
      start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
      start_time_aware = timezone.make_aware(start_time, timezone.get_default_timezone())
      end_time = request.POST.get('end_time')
      end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
      end_time_aware = timezone.make_aware(end_time, timezone.get_default_timezone())
      try:
        expected_participants = int(request.POST.get('expected_participants'))
      except ValueError:
        expected_participants = 0
      needs_projector = request.POST.get('needs_projector')
      
      message = provera(start_time_aware, end_time_aware, current_time, expected_participants,
            soba_capacity, soba_projector, needs_projector, room_id, booking_id )
      if message != None:
        messages.error(request, message)
        return render(request, 'booking/book_room.html', {'form': form})
      else:
        form.save()
        messages.success(request, 'Rezervacija je uspoešno promenjena')
        #return redirect('home')
        redirect_url = reverse('home') + '#' + str(room_id)
        return HttpResponseRedirect(redirect_url)
      
  else:
    form = BookingForm(instance=booking)

  return render(request, 'booking/book_room.html', {'form': form, 'room_name': room_name, 'edit_mode': edit_mode})
  

def check_room_availability(room_id, start_time, end_time, booking_id_to_exclude):
    room_reservations = Bookings.objects.filter(room_id=room_id)
    overlapping_reservations = room_reservations.filter(
        start_time__lt=end_time,
        end_time__gt=start_time
    ).exclude(pk=booking_id_to_exclude)
    return overlapping_reservations.exists()

def provera(start_time_aware, end_time_aware, current_time, expected_participants,
            soba_capacity, soba_projector, needs_projector, room_id, booking_id ):
  
  if start_time_aware > end_time_aware:
   return 'Ne može početak da bude posle kraja!'
  
  if start_time_aware < current_time:
    return 'Start željnog termina je u prošlosti!'
  
  if expected_participants > soba_capacity:
    return 'Treba Vam veća prostorija!'
  
  if not soba_projector and needs_projector:
    return 'Željena prostorija nema projektor!'
  
  if check_room_availability(room_id, start_time_aware, end_time_aware, booking_id):
    return 'Prostorija nije dostupna u željeno vreme'
