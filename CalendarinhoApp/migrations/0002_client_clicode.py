# Generated by Django 2.2 on 2020-03-09 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CalendarinhoApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='CliCode',
            field=models.CharField(default='9999', max_length=4),
        ),
    ]
