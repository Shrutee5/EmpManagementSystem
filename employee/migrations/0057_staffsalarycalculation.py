# Generated by Django 4.2.3 on 2023-09-16 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0056_staffsalarystructure_empname'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffSalaryCalculation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_days', models.PositiveIntegerField(default=0)),
                ('basic_a', models.FloatField(default=0.0)),
                ('hra_a', models.FloatField(default=0.0)),
                ('specialAll_a', models.FloatField(default=0.0)),
                ('grossS_a', models.FloatField(default=0.0)),
                ('others', models.FloatField(default=0.0)),
                ('incentive', models.FloatField(default=0.0)),
                ('pf_deduction', models.FloatField(default=0.0)),
                ('esic_deduction', models.FloatField(default=0.0)),
                ('other_deduction', models.FloatField(default=0.0)),
                ('gross_deduction', models.FloatField(default=0.0)),
                ('income_tax', models.FloatField(default=0.0)),
                ('netSalary', models.FloatField(default=0.0)),
                ('month', models.PositiveIntegerField(default=0)),
                ('year', models.PositiveIntegerField(default=0)),
                ('empcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employeedetail')),
            ],
        ),
    ]
