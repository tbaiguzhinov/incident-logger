# Generated by Django 4.0.6 on 2022-08-14 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hs_incidents', '0006_remove_user_email_remove_user_hash_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hs_incident',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hs_incidents.user'),
        ),
    ]
