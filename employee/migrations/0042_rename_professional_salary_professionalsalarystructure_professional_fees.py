# Generated by Django 4.2.3 on 2023-08-24 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0041_professionalsalarystructure'),
    ]

    operations = [
        migrations.RenameField(
            model_name='professionalsalarystructure',
            old_name='professional_salary',
            new_name='professional_fees',
        ),
    ]
