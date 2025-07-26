from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
import django
import os
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_project.settings')
django.setup()

from bookings.models import Booking
from hotels.models import Room
from users.models import User

app = FastAPI()

class BookingRequest(BaseModel):
    user_id: int
    room_id: int
    check_in: date
    check_out: date

@app.post('/api/book-room/')
def book_room(data: BookingRequest):
    try:
        user = User.objects.get(id=data.user_id)
        room = Room.objects.get(id=data.room_id)
    except (User.DoesNotExist, Room.DoesNotExist):
        raise HTTPException(status_code=404, detail="User or Room not found.")

    # Check if room is available for the given dates
    overlapping = Booking.objects.filter(
        room=room,
        check_in__lt=data.check_out,
        check_out__gt=data.check_in,
        status__in=["pending", "confirmed"]
    ).exists()
    if overlapping or not room.is_available:
        raise HTTPException(status_code=400, detail="Room is not available for the selected dates.")

    booking = Booking.objects.create(
        user=user,
        room=room,
        check_in=data.check_in,
        check_out=data.check_out,
        status="confirmed"
    )
    return {"booking_id": booking.id, "message": "Room booked successfully."} 