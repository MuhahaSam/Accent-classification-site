# Generated by Django 3.0.6 on 2020-05-21 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diplom', '0010_auto_20200521_0307'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='avatar')),
            ],
        ),
    ]