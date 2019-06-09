from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
from django.utils  import timezone
from jsonfield import JSONField
import uuid

def hotel_directory_path(instance, filename):
	date = timezone.now()
	return 'documents/{0}/{1}/{2}/{3}/{4}'.format(date.year, date.strftime('%B'), date.day, uuid.uuid4(), filename)

class Hotel(models.Model):
	HOTEL_TYPE_CHOICES = (
		(None, '---- Please choose hotel type ----'),
		('3 star', '3 star'),
		('4 star', '4 star'), 
		('5 star', '5 star'),
		('7 star', '7 star'),
	)
	CITY_CHOICES = (
		(None, '---- Please choose city ----'),
		('vasco', 'Vasco'), 
		('margao', 'Margao'),

	)
	name = models.CharField(max_length=45,)
	hotel_type = models.CharField(max_length=45, choices=HOTEL_TYPE_CHOICES)
	city = models.CharField(max_length=45, choices=CITY_CHOICES)
	lon = models.FloatField(verbose_name='Longitude')
	lat = models.FloatField(verbose_name='latitude')
	rating = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	description = RichTextField(verbose_name='Hotel discription', blank=True, null=True,)

	def __str__(self):
		return self.name

class Room(models.Model):
	ROOM_CHOICES = (
		(None, '---- Please choose room ----'),
		('1', 'single room'), 
		('2', 'double room'),
		('4', 'couples'),
		('3', 'family'),

	)

	room_type = models.CharField(max_length=45, choices=ROOM_CHOICES)
	room_code = models.CharField(verbose_name='Room No.', max_length=45)
	hotel = models.ForeignKey(Hotel, related_name='%(class)s_hotel', on_delete=models.CASCADE)
	description = RichTextField(verbose_name='Room Discription', blank=True, null=True,)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.room_type

	class Meta:
		unique_together = ('room_code', 'hotel')

class Images(models.Model):
	image = ThumbnailerImageField(upload_to=hotel_directory_path, max_length=500,)

	class Meta:
		abstract = True

	def __str__(self):
		return self.image.url

class RoomImages(Images):
	ROOM_IMAGE_TYPE_CHOICES = (
		(None, '---- Please choose room image type ----'),
		('bedroom', 'bedroom Image'), 
		('toilet', 'toilet Image'),
	)

	image_type = models.CharField(max_length=45, choices=ROOM_IMAGE_TYPE_CHOICES)
	room = models.ForeignKey(Room, related_name='%(class)s_room', on_delete=models.CASCADE)

	def __str__(self):
		return self.image_type

class HotelImages(Images):
	HOTEL_IMAGE_TYPE_CHOICES = (
		(None, '---- Please choose hotel image type ----'),
		('front', 'Front Image'), 
		('reception_image', 'Reception Image'),
	)

	image_type = models.CharField(max_length=45, choices=HOTEL_IMAGE_TYPE_CHOICES)
	hotel = models.ForeignKey(Hotel, related_name='%(class)s_hotel', on_delete=models.CASCADE)

	def __str__(self):
		return self.image_type

class Payment(models.Model):
	transaction_id = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	meta_data = JSONField()

	def __str__(self):
		return self.transaction_id

class Reservation(models.Model):
	STATUS_CANCELLED = 'cancelled'
	STATUS_COMPLETED = 'completed'
	STATUS_INPROCESS = 'inprocess'
	PAYMENT_STATUS_CHOICES = (
		(None, '---- Please choose status ----'),
		(STATUS_CANCELLED, 'Cancelled'), 
		(STATUS_COMPLETED, 'Completed'),
		(STATUS_INPROCESS, 'InProcess'),
	)

	check_in = models.DateTimeField()
	check_out = models.DateTimeField()
	created_on = models.DateTimeField(auto_now_add=True,)
	updated_on = models.DateTimeField(auto_now=True,)
	room = models.ForeignKey(Room, related_name='%(class)s_room', on_delete=models.CASCADE)
	created_by = models.ForeignKey(User, related_name='%(class)s_by', on_delete=models.CASCADE)
	payment = models.ForeignKey(Payment, related_name='%(class)s_payment', on_delete=models.CASCADE)
	status = models.CharField(max_length=45, choices=PAYMENT_STATUS_CHOICES, default=STATUS_INPROCESS)
	merchants_user_email = models.EmailField()
 

	def __str__(self):
		return '%s to %s' % (self.check_in, check_out)