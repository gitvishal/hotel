# Generated by Django 2.2 on 2019-05-01 06:50

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190427_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_code',
            field=models.CharField(default='1', max_length=45, verbose_name='Room No.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Room Discription'),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('room_code', 'hotel')},
        ),
    ]
