from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'room', views.RoomViewSet, base_name='room')
router.register(r'hotel', views.HotelViewSet, base_name='hotel')
router.register(r'room-image', views.RoomImagesViewSet, base_name='room-image')
router.register(r'hotel-image', views.HotelImagesViewSet, base_name='hotel-image')
router.register(r'reservation', views.ReservationViewSet, base_name='reservation')

urlpatterns = [
	path('v1/', include(router.urls)),
	path('v1/city-<city>/', include(router.urls)),
	path('v1/type-<room_type>/', include(router.urls)),
	path('v1/city-<city>/type-<room_type>/', include(router.urls)),
	path('obtain-auth-token/', views.HotelAuthToken.as_view(), name='obtain-auth-token'),
	path('city/', views.CityView.as_view(), name='city'),
	path('room-type/', views.RoomTypeView.as_view(), name='room-type'),
	path('last-reservation/<int:pk>/', views.LastReservation.as_view(), name='last-reservation'),
]
