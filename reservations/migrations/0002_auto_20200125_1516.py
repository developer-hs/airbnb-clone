# Generated by Django 2.2.5 on 2020-01-25 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending(미결)'), ('confirmed', 'Confirmed(확인)'), ('canceled', 'Canceled(취소)')], default='pending', max_length=12),
        ),
    ]