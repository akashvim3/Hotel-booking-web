from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from .models import Booking
from django.utils import timezone

@shared_task
def send_booking_confirmation(booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
        
        # Render email template
        context = {
            'booking': booking,
            'user': booking.user,
            'hotel': booking.room.hotel,
            'room': booking.room
        }
        
        html_message = render_to_string('bookings/email/confirmation.html', context)
        plain_message = render_to_string('bookings/email/confirmation.txt', context)
        
        # Send email
        send_mail(
            subject=f'Booking Confirmation - {booking.room.hotel.name}',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.user.email],
            html_message=html_message
        )
        
        # Update booking notification status
        booking.confirmation_sent = True
        booking.save(update_fields=['confirmation_sent'])
        
    except Booking.DoesNotExist:
        pass  # Log error or handle appropriately

@shared_task
def send_booking_reminder():
    """Send reminder emails for upcoming bookings"""
    tomorrow = timezone.now() + timezone.timedelta(days=1)
    upcoming_bookings = Booking.objects.filter(
        check_in=tomorrow.date(),
        status='confirmed',
        reminder_sent=False
    )
    
    for booking in upcoming_bookings:
        context = {
            'booking': booking,
            'user': booking.user,
            'hotel': booking.room.hotel,
            'room': booking.room
        }
        
        html_message = render_to_string('bookings/email/reminder.html', context)
        plain_message = render_to_string('bookings/email/reminder.txt', context)
        
        send_mail(
            subject=f'Reminder: Your stay at {booking.room.hotel.name} tomorrow',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.user.email],
            html_message=html_message
        )
        
        booking.reminder_sent = True
        booking.save(update_fields=['reminder_sent'])
