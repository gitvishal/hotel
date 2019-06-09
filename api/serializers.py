from rest_framework import serializers
from django.db import transaction
from .models import *

class RoomImagesSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='api:room-image-detail')
	room = serializers.HyperlinkedIdentityField(view_name='api:room-detail')

	class Meta:
		model = RoomImages 
		fields = '__all__'

class RoomSerializer(serializers.HyperlinkedModelSerializer):
	room_pk = serializers.ReadOnlyField(source='pk')
	url = serializers.HyperlinkedIdentityField(view_name='api:room-detail')
	hotel = serializers.HyperlinkedIdentityField(view_name='api:hotel-detail')
	roomimages_room = serializers.HyperlinkedRelatedField(
		many=True,
		read_only=True,
		view_name='api:room-image-detail'
	)

	class Meta:
		model = Room 
		fields = '__all__'

class HotelImagesSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='api:hotel-image-detail')
	hotel = serializers.HyperlinkedIdentityField(view_name='api:hotel-detail')

	class Meta:
		model = HotelImages 
		fields = '__all__'

class HotelSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='api:hotel-detail')
	hotelimages_hotel = serializers.HyperlinkedRelatedField(
		many=True,
		read_only=True,
		view_name='api:hotel-image-detail'
	)

	class Meta:
		model = Hotel 
		fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Payment 
		fields = ('meta_data',)

class ReservationSerializer(serializers.ModelSerializer):
	payment = PaymentSerializer()

	def create(self, validated_data):
		payment = validated_data.pop('payment')
		room = validated_data['room']
		duration = validated_data['check_out'] - validated_data['check_in']

		with transaction.atomic():
			payment = Payment.objects.create(
				transaction_id=uuid.uuid4().hex,
				price=duration*room.price, 
				**payment
			)
			reservation = Reservation.objects.create(
				payment=payment,
				status=Reservation.STATUS_COMPLETED,
				**validated_data
			)

		return reservation

	def validate(self, attrs):
		check_in = attrs.get('check_in')
		check_out = attrs.get('check_out')
		room = attrs.get('room')

		res = Reservation.objects.filter(
			room=room, 
			status=Reservation.STATUS_COMPLETED,
			check_out__gte=check_in
		)

		if res.exists():
			raise serializers.ValidationError('room already occupied')

		return attrs
	
	class Meta:
		model = Reservation 
		exclude = ('created_by', )
