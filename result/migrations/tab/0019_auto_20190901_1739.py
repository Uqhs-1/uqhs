# Generated by Django 2.1.3 on 2019-09-01 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0018_auto_20190901_0818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annual',
            name='subject',
        ),
        migrations.AddField(
            model_name='annual',
            name='term',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]