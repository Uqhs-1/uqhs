# Generated by Django 2.1.3 on 2019-12-23 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0063_auto_20191223_1550'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('subjects',)},
        ),
        migrations.RemoveField(
            model_name='question',
            name='teacher_name',
        ),
        migrations.AddField(
            model_name='question',
            name='classes',
            field=models.CharField(default='Undefined', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='subjects',
            field=models.CharField(default='Undefined', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='terms',
            field=models.CharField(default='Undefined', max_length=200, null=True),
        ),
    ]
