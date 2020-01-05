# Generated by Django 2.2.9 on 2020-01-04 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0028_auto_20200103_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='positions',
        ),
        migrations.AddField(
            model_name='position',
            name='project',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='teams.Project'),
        ),
        migrations.AlterField(
            model_name='position',
            name='description',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
