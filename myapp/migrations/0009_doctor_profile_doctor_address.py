# Generated by Django 4.0.5 on 2022-07-03 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_doctor_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor_profile',
            name='doctor_address',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
