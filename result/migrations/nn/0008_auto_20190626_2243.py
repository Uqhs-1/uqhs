# Generated by Django 2.1.3 on 2019-06-26 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0007_auto_20190626_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btutor',
            name='session',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
