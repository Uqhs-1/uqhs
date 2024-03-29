# Generated by Django 5.0.1 on 2024-01-07 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2024-01-07', max_length=200),
        ),
        migrations.AlterField(
            model_name='edit_user',
            name='resumption',
            field=models.DateField(blank=True, default='2024-01-07', help_text='Date format: MM/DD/YYYY', null=True),
        ),
    ]
