# Generated by Django 4.2.3 on 2023-08-07 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0013_alter_attend_is_present'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyforleave',
            name='biMOB',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='biMOT',
            field=models.PositiveIntegerField(default=2),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='earnedLeaveB',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='earnedLeaveT',
            field=models.PositiveIntegerField(default=36),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='ffcB',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='ffcT',
            field=models.PositiveIntegerField(default=4),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='maternityLB',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='maternityLT',
            field=models.PositiveIntegerField(default=182),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='oH2B',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='oH2T',
            field=models.PositiveIntegerField(default=2),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='oHB',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='oHT',
            field=models.PositiveIntegerField(default=2),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='sickLeaveB',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applyforleave',
            name='sickLeaveT',
            field=models.PositiveIntegerField(default=7),
        ),
    ]
