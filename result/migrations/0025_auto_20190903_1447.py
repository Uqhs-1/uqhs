# Generated by Django 2.1.3 on 2019-09-03 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0024_auto_20190903_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='btutor',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('delete', 'Delete')], default='active', help_text='Acount Status', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='session',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
