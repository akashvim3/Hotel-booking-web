from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Room, HotelImage, RoomImage, Amenity
from django.contrib.auth.decorators import login_required
from .forms import HotelForm, RoomForm
from django.forms import modelformset_factory
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from bookings.models import Booking

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    rooms = hotel.room_set.all()
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})

@login_required
def hotel_create(request):
    HotelImageFormSet = modelformset_factory(HotelImage, fields=('image',), extra=3, max_num=5)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        formset = HotelImageFormSet(request.POST, request.FILES, queryset=HotelImage.objects.none())
        if form.is_valid() and formset.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            form.save_m2m()
            for img_form in formset:
                if img_form.cleaned_data:
                    HotelImage.objects.create(hotel=hotel, image=img_form.cleaned_data['image'])
            return redirect('hotel_list')
    else:
        form = HotelForm()
        formset = HotelImageFormSet(queryset=HotelImage.objects.none())
    return render(request, 'hotels/hotel_form.html', {'form': form, 'formset': formset})

@login_required
def hotel_update(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk, owner=request.user)
    HotelImageFormSet = modelformset_factory(HotelImage, fields=('image',), extra=3, max_num=5)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        formset = HotelImageFormSet(request.POST, request.FILES, queryset=hotel.images.all())
        if form.is_valid() and formset.is_valid():
            form.save()
            for img_form in formset:
                if img_form.cleaned_data and img_form.cleaned_data.get('image'):
                    HotelImage.objects.create(hotel=hotel, image=img_form.cleaned_data['image'])
            return redirect('hotel_detail', pk=hotel.pk)
    else:
        form = HotelForm(instance=hotel)
        formset = HotelImageFormSet(queryset=hotel.images.all())
    return render(request, 'hotels/hotel_form.html', {'form': form, 'formset': formset})

@login_required
def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk, owner=request.user)
    if request.method == 'POST':
        hotel.delete()
        return redirect('hotel_list')
    return render(request, 'hotels/hotel_confirm_delete.html', {'hotel': hotel})

@login_required
def room_create(request, hotel_pk):
    hotel = get_object_or_404(Hotel, pk=hotel_pk, owner=request.user)
    RoomImageFormSet = modelformset_factory(RoomImage, fields=('image',), extra=3, max_num=5)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        formset = RoomImageFormSet(request.POST, request.FILES, queryset=RoomImage.objects.none())
        if form.is_valid() and formset.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            form.save_m2m()
            for img_form in formset:
                if img_form.cleaned_data:
                    RoomImage.objects.create(room=room, image=img_form.cleaned_data['image'])
            return redirect('hotel_detail', pk=hotel.pk)
    else:
        form = RoomForm()
        formset = RoomImageFormSet(queryset=RoomImage.objects.none())
    return render(request, 'hotels/room_form.html', {'form': form, 'formset': formset, 'hotel': hotel})

@login_required
def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk, hotel__owner=request.user)
    RoomImageFormSet = modelformset_factory(RoomImage, fields=('image',), extra=3, max_num=5)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        formset = RoomImageFormSet(request.POST, request.FILES, queryset=room.images.all())
        if form.is_valid() and formset.is_valid():
            form.save()
            for img_form in formset:
                if img_form.cleaned_data and img_form.cleaned_data.get('image'):
                    RoomImage.objects.create(room=room, image=img_form.cleaned_data['image'])
            return redirect('hotel_detail', pk=room.hotel.pk)
    else:
        form = RoomForm(instance=room)
        formset = RoomImageFormSet(queryset=room.images.all())
    return render(request, 'hotels/room_form.html', {'form': form, 'formset': formset, 'hotel': room.hotel})

@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk, hotel__owner=request.user)
    hotel_pk = room.hotel.pk
    if request.method == 'POST':
        room.delete()
        return redirect('hotel_detail', pk=hotel_pk)
    return render(request, 'hotels/room_confirm_delete.html', {'room': room})

def search(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rating = request.GET.get('rating')
    amenities = request.GET.getlist('amenities')
    room_type = request.GET.get('room_type')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    hotels = Hotel.objects.all()
    if query:
        hotels = hotels.filter(Q(name__icontains=query) | Q(city__icontains=query) | Q(description__icontains=query))
    if amenities:
        hotels = hotels.filter(amenities__in=amenities).distinct()
    if rating:
        hotels = hotels.filter(reviews__rating__gte=rating).distinct()
    if min_price or max_price or room_type or check_in or check_out:
        hotels = hotels.filter(room__is_available=True)
        if min_price:
            hotels = hotels.filter(room__price__gte=min_price)
        if max_price:
            hotels = hotels.filter(room__price__lte=max_price)
        if room_type:
            hotels = hotels.filter(room__room_type=room_type)
        # Real-time availability logic can be added here
    hotels = hotels.distinct()
    return render(request, 'search.html', {'results': hotels})

@require_GET
def api_search_rooms(request):
    city = request.GET.get('city')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    guests = int(request.GET.get('guests', 1))

    # Filter hotels by city
    hotels = Hotel.objects.filter(city__icontains=city) if city else Hotel.objects.all()

    # Find available rooms
    available_rooms = Room.objects.filter(hotel__in=hotels, is_available=True)
    if check_in and check_out:
        # Exclude rooms with overlapping bookings
        overlapping = Booking.objects.filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in),
            status='confirmed'
        ).values_list('room_id', flat=True)
        available_rooms = available_rooms.exclude(id__in=overlapping)

    # Optionally filter by guests if you have a capacity field
    # available_rooms = available_rooms.filter(capacity__gte=guests)

    # Prepare response
    data = []
    for room in available_rooms.select_related('hotel'):
        data.append({
            'hotel': room.hotel.name,
            'hotel_id': room.hotel.id,
            'room_id': room.id,
            'room_type': room.room_type,
            'price': str(room.price),
            'city': room.hotel.city,
            'image': room.image.url if room.image else '',
        })
    return JsonResponse({'results': data})
