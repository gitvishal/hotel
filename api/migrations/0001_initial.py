# Generated by Django 2.2 on 2019-04-27 11:24

import api.models
import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='City Name')),
                ('hotel_type', models.CharField(choices=[(None, '---- Please choose hotel type ----'), ('3', '3 star'), ('5', '5 star'), ('7', '7 star')], max_length=45)),
                ('city', models.CharField(choices=[(None, '---- Please choose city ----'), ('vasco', 'Vasco'), ('margao', 'Margao')], max_length=45)),
                ('lon', models.FloatField(verbose_name='Longitude')),
                ('lat', models.FloatField(verbose_name='latitude')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='room discription')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(choices=[(None, '---- Please choose room ----'), ('1bhk', '1 BHK'), ('2', '2 BHK')], max_length=45)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(max_length=500, upload_to=api.models.hotel_directory_path)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='room discription')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_hotel', to='api.Hotel')),
            ],
        ),
        migrations.CreateModel(
            name='RoomImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(max_length=500, upload_to=api.models.hotel_directory_path)),
                ('image_type', models.CharField(choices=[(None, '---- Please choose room image type ----'), ('bedroom', 'bedroom Image'), ('toilet', 'toilet Image')], max_length=45)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roomimages_room', to='api.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(max_length=500, upload_to=api.models.hotel_directory_path)),
                ('image_type', models.CharField(choices=[(None, '---- Please choose hotel image type ----'), ('front', 'Front Image'), ('reception_image', 'Reception Image')], max_length=45)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotelimages_hotel', to='api.Hotel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
