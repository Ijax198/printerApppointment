# Generated by Django 4.2 on 2023-07-02 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_remove_printer_pcapacity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='time_in',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='time_out',
        ),
    ]