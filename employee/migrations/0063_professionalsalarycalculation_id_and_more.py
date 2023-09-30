# Generated by Django 4.2.3 on 2023-09-18 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0062_staffsalarycalculation_empname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionalsalarycalculation',
            name='id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='salarycalculation',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffsalary',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='professionalsalarycalculation',
            name='empcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employeedetail'),
        ),
        migrations.AlterField(
            model_name='salarycalculation',
            name='staff_salary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.staffsalary'),
        ),
        migrations.AlterField(
            model_name='staffsalary',
            name='empcode',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employee.employeedetail'),
        ),
    ]
