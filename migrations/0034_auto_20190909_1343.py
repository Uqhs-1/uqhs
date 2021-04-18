# Generated by Django 2.1.3 on 2019-09-09 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0033_auto_20190905_1825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registered_id',
            options={'ordering': ('student_class',)},
        ),
        migrations.AddField(
            model_name='overall_annual',
            name='created',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2019-09-09', max_length=200),
        ),
        migrations.AlterField(
            model_name='session',
            name='created',
            field=models.DateTimeField(default='2019-09-09', max_length=200),
        ),
    ]
