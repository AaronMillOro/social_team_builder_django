# Generated by Django 2.2.9 on 2020-01-07 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20200107_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='related_skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Skill'),
        ),
    ]