# Generated by Django 4.0.6 on 2022-08-12 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hs_incidents', '0004_alter_injury_relation_to_business_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hs_incident',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='hs_incidents.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hs_incident',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='hs_incident',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude'),
        ),
    ]