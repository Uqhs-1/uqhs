# Generated by Django 2.1.3 on 2020-06-30 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0101_auto_20200626_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='btutor',
            name='first_term',
            field=models.CharField(blank=True, default='1st Term', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='btutor',
            name='second_term',
            field=models.CharField(blank=True, default='1st Term', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='btutor',
            name='third_term',
            field=models.CharField(blank=True, default='1st Term', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='annual',
            name='term',
            field=models.CharField(blank=True, help_text='Select subject term', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2020-06-30', max_length=200),
        ),
        migrations.AlterField(
            model_name='downloadformat',
            name='created',
            field=models.DateTimeField(default='2020-06-30', max_length=200),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='term',
            field=models.CharField(blank=True, default='1st Term', max_length=30, null=True),
        ),
    ]
