# Generated by Django 2.2.13 on 2021-04-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0134_auto_20210205_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2021-04-18', max_length=200),
        ),
        migrations.AlterField(
            model_name='edit_user',
            name='resumption',
            field=models.DateField(blank=True, default='2021-04-18', help_text='Date format: MM/DD/YYYY', null=True),
        ),
    ]
