# Generated by Django 4.2.3 on 2023-09-22 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0063_professionalsalarycalculation_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffsalarycalculation',
            name='month_int',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
