# Generated by Django 2.1.3 on 2020-08-01 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0127_cname_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='cname',
            name='p_name',
            field=models.CharField(blank=True, default='OLAGUNJU MUSLIM', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cname',
            name='full_name',
            field=models.CharField(blank=True, default='Surname', max_length=200, null=True),
        ),
    ]
