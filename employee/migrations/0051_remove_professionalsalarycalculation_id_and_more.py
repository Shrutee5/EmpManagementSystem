# Generated by Django 4.2.3 on 2023-09-14 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0050_alter_employeedetail_accountno_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professionalsalarycalculation',
            name='id',
        ),
        migrations.RemoveField(
            model_name='professionalsalarycalculation',
            name='payDaysA',
        ),
    ]
