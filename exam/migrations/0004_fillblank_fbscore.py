# Generated by Django 2.1.1 on 2018-09-04 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_auto_20180904_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='fillblank',
            name='fbScore',
            field=models.FloatField(null=True, verbose_name='分数'),
        ),
    ]