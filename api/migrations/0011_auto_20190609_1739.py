# Generated by Django 2.2 on 2019-06-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_payment_payment_merchant_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[(None, '---- Please choose status ----'), ('cancelled', 'Cancelled'), ('completed', 'Completed'), ('inprocess', 'InProcess')], default='inprocess', max_length=45),
        ),
    ]
