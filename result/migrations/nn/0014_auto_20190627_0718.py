# Generated by Django 2.1.3 on 2019-06-26 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0013_auto_20190627_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='avr',
            field=models.FloatField(blank=True, default='0', max_length=8, null=True),
        ),
    ]
