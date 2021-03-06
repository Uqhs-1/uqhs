# Generated by Django 2.1.3 on 2020-06-17 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0098_auto_20200527_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='qsubject',
            name='aagr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='qsubject',
            name='avr',
            field=models.FloatField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='qsubject',
            name='fagr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='qsubject',
            name='sagr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2020-06-18', max_length=200),
        ),
        migrations.AlterField(
            model_name='downloadformat',
            name='created',
            field=models.DateTimeField(default='2020-06-18', max_length=200),
        ),
    ]
