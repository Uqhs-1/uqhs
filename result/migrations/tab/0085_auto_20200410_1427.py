# Generated by Django 2.1.3 on 2020-04-10 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0084_auto_20200409_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2020-04-10', max_length=200),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='resumption',
            field=models.CharField(blank=True, default='Monday January 9, 2017.', help_text='Next term begings.', max_length=115, null=True),
        ),
        migrations.AlterField(
            model_name='downloadformat',
            name='created',
            field=models.DateTimeField(default='2020-04-10', max_length=200),
        ),
    ]