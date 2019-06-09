from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.generic import View
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets, permissions, authentication
from datetime import timedelta
from django.db.models import Max
from .models import *
from .serializers import *
from django.db.models import Q
import functools
import operator

class CityView(View):
	def get(self, *args, **kwargs):
		return JsonResponse(dict(filter(lambda x:x[0], Hotel.CITY_CHOICES)))

class LastReservation(View):
	def get(self, pk, *args, **kwargs):
		try:
			room = Room.objects.get(pk=pk)
			last_checkout = Reservation.objects.filter(
				room=room, 
				status=Reservation.STATUS_COMPLETED
			).aggregate(ckout=Max('check_out'))
			return Response({'last_checkout':last_checkout['ckout'] + timedelta(hours=3)})
		except Room.DoesNotExists as e:
			return Response({"Error": "Field does not exists"}, status=status.HTTP_404_NOT_FOUND)


class RoomTypeView(View):
	def get(self, *args, **kwargs):
		return JsonResponse(dict(filter(lambda x:x[0], Room.ROOM_CHOICES)))
		
class RoomViewSet(viewsets.ReadOnlyModelViewSet):
	city = None
	room_type = None
	search = None
	queryset = Room.objects.all()
	serializer_class = RoomSerializer

	def get_queryset(self):
		self.queryset = self.queryset.filter(hotel__city=self.city) if self.city else self.queryset
		self.queryset = self.queryset.filter(room_type=self.room_type) if self.room_type else self.queryset
		self.queryset = self.queryset.filter(
			functools.reduce(
				operator.and_,
				(
					Q(room_type__icontains=s.strip())|
					Q(hotel__name__icontains=s.strip())|
					Q(hotel__hotel_type__icontains=s.strip())|
					Q(description__icontains=s.strip())|
					Q(hotel__description__icontains=s.strip())|
					Q(hotel__city__icontains=s.strip())

					for s in self.search.split() if s.strip()
				)
			)
		) if self.search else self.queryset
		return self.queryset

	def list(self, *args, **kwargs):
		self.search = self.request.GET.get('s')
		self.city = kwargs.pop('city', None)
		self.room_type = kwargs.pop('room_type', None)
		return super(RoomViewSet, self).list(*args, **kwargs)

class HotelViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Hotel.objects.all()
	serializer_class = HotelSerializer

class RoomImagesViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = RoomImages.objects.all()
	serializer_class = RoomImagesSerializer

class HotelImagesViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = HotelImages.objects.all()
	serializer_class = HotelImagesSerializer

class ReservationViewSet(viewsets.ModelViewSet):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

class HotelAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })