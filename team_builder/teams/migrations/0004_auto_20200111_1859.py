# Generated by Django 2.2.9 on 2020-01-11 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20200107_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(default='Waiting response', max_length=2),
        ),
    ]