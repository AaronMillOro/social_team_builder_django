# Generated by Django 2.2.7 on 2019-12-10 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20191210_0226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='skills_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='skills_name',
            field=models.CharField(default='', max_length=500, verbose_name='Skill'),
        ),
    ]