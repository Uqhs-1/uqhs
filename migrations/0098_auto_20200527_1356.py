# Generated by Django 2.1.3 on 2020-05-27 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0097_auto_20200430_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2020-05-27', max_length=200),
        ),
        migrations.AlterField(
            model_name='downloadformat',
            name='created',
            field=models.DateTimeField(default='2020-05-27', max_length=200),
        ),
    ]
