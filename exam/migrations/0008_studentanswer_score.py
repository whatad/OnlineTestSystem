# Generated by Django 2.1.1 on 2018-09-06 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_auto_20180906_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswer',
            name='score',
            field=models.FloatField(default=0),
        ),
    ]
