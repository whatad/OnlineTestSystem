# Generated by Django 2.1.1 on 2018-09-06 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_auto_20180906_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentanswer',
            name='fillBlankId',
            field=models.IntegerField(default=0),
        ),
    ]