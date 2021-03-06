# Generated by Django 2.1.3 on 2020-07-16 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0109_auto_20200716_0446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qsubject',
            name='annual_avg',
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='agn',
            field=models.FloatField(blank=True, default=0, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='agr',
            field=models.FloatField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='annual_scores',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='atd',
            field=models.FloatField(blank=True, default=0, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='exam',
            field=models.FloatField(blank=True, default=0, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='test',
            field=models.FloatField(blank=True, default=0, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='total',
            field=models.FloatField(blank=True, default=0, max_length=4, null=True),
        ),
    ]
