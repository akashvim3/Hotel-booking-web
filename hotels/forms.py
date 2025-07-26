from django import forms
from .models import Hotel, Room, Amenity, HotelImage, RoomImage

class HotelForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(queryset=Amenity.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'city', 'description', 'image', 'amenities']

class RoomForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(queryset=Amenity.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Room
        fields = ['hotel', 'room_type', 'price', 'is_available', 'image', 'amenities']
