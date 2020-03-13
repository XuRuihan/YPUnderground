# Generated by Django 3.0.3 on 2020-03-01 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='Rstatus',
            field=models.SmallIntegerField(choices=[(0, 'Permitted'), (1, 'Suspended'), (2, 'Forbidden')], default=0, verbose_name='房间状态'),
        ),
    ]
