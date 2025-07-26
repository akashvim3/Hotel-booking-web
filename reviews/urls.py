from . import views
from django.urls import path

urlpatterns = [
    path('add/', views.add_review, name='add_review'),
    path('add/<int:hotel_id>/', views.add_review, name='add_review_for_hotel'),
]
