# Generated by Django 2.1.3 on 2020-04-21 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0095_auto_20200419_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2020-04-21', max_length=200),
        ),
        migrations.AlterField(
            model_name='downloadformat',
            name='created',
            field=models.DateTimeField(default='2020-04-21', max_length=200),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='event',
            field=models.CharField(blank=True, default='_____', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='indoor',
            field=models.CharField(blank=True, default='_____', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='jump',
            field=models.CharField(blank=True, default='_____', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='throw',
            field=models.CharField(blank=True, default='_____', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='track',
            field=models.CharField(blank=True, default='_____', max_length=10, null=True),
        ),
    ]
