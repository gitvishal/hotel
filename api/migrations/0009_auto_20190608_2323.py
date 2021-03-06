# Generated by Django 2.2 on 2019-06-08 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190607_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='merchants_user_email',
            field=models.EmailField(default='a@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='BookingUser',
        ),
    ]
