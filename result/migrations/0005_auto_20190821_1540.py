# Generated by Django 2.1.3 on 2019-08-21 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0004_auto_20190820_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cname',
            old_name='model_summary',
            new_name='full_name',
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2019-08-21', max_length=200),
        ),
    ]
