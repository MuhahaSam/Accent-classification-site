# Generated by Django 3.0.6 on 2020-05-23 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diplom', '0015_delete_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='result',
            field=models.FloatField(),
        ),
    ]
