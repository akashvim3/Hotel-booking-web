from . import views
from django.urls import path

urlpatterns = [
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('pay/<int:booking_id>/', views.pay_for_booking, name='pay_for_booking'),
]
