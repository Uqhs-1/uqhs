# Generated by Django 2.1.3 on 2020-01-20 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0075_auto_20200120_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='photo',
            field=models.ImageField(default='Undefined', null=True, upload_to='static/result/question_image/'),
        ),
    ]