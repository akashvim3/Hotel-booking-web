from django.contrib import admin
from .models import Hotel, Room, HotelImage, RoomImage

class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInline]

class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(HotelImage)
admin.site.register(RoomImage)
