# Generated by Django 2.2.9 on 2020-01-05 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0035_auto_20200105_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Project'),
        ),
    ]
