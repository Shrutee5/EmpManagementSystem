# Generated by Django 4.2.3 on 2023-09-22 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0064_staffsalarycalculation_month_int'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionalsalarycal',
            name='month_int',
            field=models.PositiveIntegerField(default=0),
        ),
    ]