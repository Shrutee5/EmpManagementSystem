# Generated by Django 4.2.3 on 2023-09-16 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0052_professionalsalarycalculation_grossded_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professionalsalarycalculation',
            name='empcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='employee.employeedetail'),
        ),
    ]
