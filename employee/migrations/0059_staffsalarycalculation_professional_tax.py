# Generated by Django 4.2.3 on 2023-09-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0058_alter_staffsalarycalculation_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffsalarycalculation',
            name='professional_tax',
            field=models.FloatField(default=0.0),
        ),
    ]
