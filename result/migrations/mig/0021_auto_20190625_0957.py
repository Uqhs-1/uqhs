# Generated by Django 2.1.3 on 2019-06-24 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0020_auto_20190625_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='first',
            field=models.FloatField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='second',
            field=models.FloatField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='third',
            field=models.FloatField(blank=True, max_length=8, null=True),
        ),
    ]
