# Generated by Django 2.1.3 on 2020-06-26 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0100_auto_20200623_0443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qsubject',
            name='Class',
        ),
        migrations.AddField(
            model_name='qsubject',
            name='term',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2020-06-26', max_length=200),
        ),
        migrations.AlterField(
            model_name='downloadformat',
            name='created',
            field=models.DateTimeField(default='2020-06-26', max_length=200),
        ),
    ]
