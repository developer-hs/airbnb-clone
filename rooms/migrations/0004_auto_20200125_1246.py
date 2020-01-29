# Generated by Django 2.2.5 on 2020-01-25 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_auto_20200125_1227'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amenity',
            options={'verbose_name_plural': 'Amenityes'},
        ),
        migrations.AlterModelOptions(
            name='facility',
            options={'verbose_name_plural': 'Facilitys'},
        ),
        migrations.AlterModelOptions(
            name='houserule',
            options={'verbose_name': 'House Rule'},
        ),
        migrations.AlterModelOptions(
            name='roomtype',
            options={'verbose_name': 'Room Type'},
        ),
        migrations.AlterField(
            model_name='room',
            name='amenitys',
            field=models.ManyToManyField(blank=True, to='rooms.Amenity'),
        ),
        migrations.AlterField(
            model_name='room',
            name='facilitys',
            field=models.ManyToManyField(blank=True, to='rooms.Facility'),
        ),
        migrations.AlterField(
            model_name='room',
            name='houserules',
            field=models.ManyToManyField(blank=True, to='rooms.HouseRule'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('caption', models.CharField(max_length=80)),
                ('file', models.ImageField(upload_to='')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
