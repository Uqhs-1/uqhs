# Generated by Django 2.1.3 on 2020-04-17 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0089_auto_20200417_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_info',
            name='gender',
            field=models.CharField(blank=True, default='Male', max_length=10, null=True),
        ),
    ]