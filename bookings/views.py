from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking
from .forms import BookingForm
from hotels.models import Room
from django.utils import timezone
from .payment import create_payment_intent
from .models import Payment

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id, is_available=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            # Check availability
            overlapping = Booking.objects.filter(
                room=room,
                check_in__lt=booking.check_out,
                check_out__gt=booking.check_in,
                status='confirmed'
            )
            if overlapping.exists():
                form.add_error(None, 'Room is not available for the selected dates.')
            else:
                booking.status = 'confirmed'
                booking.save()
                room.is_available = False
                room.save()
                return redirect('user_dashboard')
    else:
        form = BookingForm()
    return render(request, 'bookings/book_room.html', {'form': form, 'room': room})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            new_booking = form.save(commit=False)
            # Check for overlapping bookings
            overlapping = Booking.objects.filter(
                room=booking.room,
                check_in__lt=new_booking.check_out,
                check_out__gt=new_booking.check_in,
                status='confirmed'
            ).exclude(pk=booking.pk)
            if overlapping.exists():
                form.add_error(None, 'Room is not available for the selected dates.')
            else:
                new_booking.save()
                return redirect('user_dashboard')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'bookings/book_room.html', {'form': form, 'room': booking.room, 'edit': True})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        booking.room.is_available = True
        booking.room.save()
        # Optionally trigger refund/payment logic here
        return redirect('user_dashboard')
    return render(request, 'bookings/booking_confirm_cancel.html', {'booking': booking})

@login_required
def pay_for_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if booking.status != 'confirmed':
        return redirect('user_dashboard')
    if request.method == 'POST':
        # Here you would integrate with Stripe or another payment gateway
        # For demo, we mark as paid and create a Payment record
        Payment.objects.create(
            booking=booking,
            user=request.user,
            amount=booking.room.price,
            status='succeeded',
            payment_method='stripe'
        )
        booking.status = 'paid'
        booking.save()
        return redirect('user_dashboard')
    return render(request, 'bookings/pay.html', {'booking': booking})
