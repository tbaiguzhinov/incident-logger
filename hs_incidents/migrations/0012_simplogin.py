# Generated by Django 4.0.6 on 2022-09-06 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hs_incidents', '0011_illness_injury_delete_injury_or_illness'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField(verbose_name='токен')),
            ],
        ),
    ]
