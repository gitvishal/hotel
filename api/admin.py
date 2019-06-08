from django.contrib import admin
from api.models import *

@admin.register(Hotel)
class AdminHotel(admin.ModelAdmin):
	list_per_page = 15

	search_fields = ('name', 'hotel_type', 'city',)
	list_filter = ('name', 'hotel_type', 'city',)
	readonly_fields = ('rating', )

@admin.register(Room)
class AdminRoom(admin.ModelAdmin):
	list_per_page = 15

	search_fields = ('room_type', 'hotel',)
	list_filter = ('room_type', 'hotel',)

@admin.register(RoomImages)
class AdminRoomImages(admin.ModelAdmin):
	list_per_page = 15

	search_fields = ('image_type', 'room',)
	list_filter = ('room',  'image_type',)

@admin.register(HotelImages)
class AdminHotelImages(admin.ModelAdmin):
	list_per_page = 15

	search_fields = ('image_type', 'hotel',)
	list_filter = ('image_type', 'hotel',)
