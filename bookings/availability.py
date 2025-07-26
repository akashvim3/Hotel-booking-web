from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from .models import Booking
from hotels.models import Room
import json

@require_http_methods(["POST"])
def check_room_availability(request):
    data = json.loads(request.body)
    room_id = data.get('room_id')
    check_in = datetime.strptime(data.get('check_in'), '%Y-%m-%d').date()
    check_out = datetime.strptime(data.get('check_out'), '%Y-%m-%d').date()
    
    try:
        room = Room.objects.get(pk=room_id)
        # Check for overlapping bookings
        overlapping = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
            status='confirmed'
        ).exists()
        
        if overlapping:
            return JsonResponse({
                'available': False,
                'message': 'Room is not available for the selected dates.'
            })
        
        # Calculate total price
        days = (check_out - check_in).days
        total_price = room.price * days
        
        return JsonResponse({
            'available': True,
            'total_price': float(total_price),
            'message': 'Room is available!'
        })
    except Room.DoesNotExist:
        return JsonResponse({
            'available': False,
            'message': 'Room not found.'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'available': False,
            'message': str(e)
        }, status=400)

@login_required
@require_http_methods(["POST"])
def hold_room(request):
    """Temporarily hold a room for 15 minutes while user completes booking"""
    data = json.loads(request.body)
    room_id = data.get('room_id')
    check_in = datetime.strptime(data.get('check_in'), '%Y-%m-%d').date()
    check_out = datetime.strptime(data.get('check_out'), '%Y-%m-%d').date()
    
    try:
        room = Room.objects.get(pk=room_id)
        # Create a temporary booking
        booking = Booking.objects.create(
            user=request.user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            status='pending',
            expires_at=timezone.now() + timezone.timedelta(minutes=15)
        )
        
        return JsonResponse({
            'success': True,
            'booking_id': booking.id,
            'message': 'Room held for 15 minutes'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
