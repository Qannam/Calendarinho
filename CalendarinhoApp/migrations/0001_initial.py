# Generated by Django 2.2.10 on 2020-03-03 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CliName', models.CharField(max_length=200)),
                ('CliShort', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EmpName', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Note', models.CharField(max_length=200)),
                ('StartDate', models.DateField(verbose_name='Start Date')),
                ('EndDate', models.DateField(verbose_name='End Date')),
                ('LeaveType', models.CharField(choices=[('Training', 'Training'), ('Vacation', 'Vacation')], default='Vacation', max_length=8)),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CalendarinhoApp.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Engagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EngName', models.CharField(max_length=200)),
                ('ServiceType', models.CharField(choices=[('Non', '--'), ('WVA', 'Web Vulnerability Asseessment'), ('WPT', 'Web Penetration Testing'), ('SCR', 'Source Code Review'), ('NVA', 'Network Vulnerability Asseessment'), ('NPT', 'Network Penetration Testing')], default='Non', max_length=3)),
                ('StartDate', models.DateField(verbose_name='Start Date')),
                ('EndDate', models.DateField(verbose_name='End Date')),
                ('CliName', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='CalendarinhoApp.Client')),
                ('Employees', models.ManyToManyField(blank=True, related_name='Engagements', to='CalendarinhoApp.Employee')),
            ],
        ),
    ]
