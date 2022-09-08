# Generated by Django 4.0.6 on 2022-08-14 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hs_incidents', '0007_alter_hs_incident_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='injury',
            options={'verbose_name_plural': 'Injuries'},
        ),
        migrations.AlterField(
            model_name='hs_incident',
            name='date_created',
            field=models.DateField(verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='hs_incident',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='hs_incidents.user'),
        ),
        migrations.AlterField(
            model_name='illness',
            name='incident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='illnesses', to='hs_incidents.hs_incident', verbose_name='Incident'),
        ),
        migrations.AlterField(
            model_name='injury',
            name='incident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='injuries', to='hs_incidents.hs_incident', verbose_name='Incident'),
        ),
    ]