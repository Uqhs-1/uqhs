# Generated by Django 2.1.3 on 2019-09-01 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0019_auto_20190901_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annual',
            name='term',
            field=models.CharField(blank=True, choices=[('1st Term', 'first term'), ('2nd Term', 'second term'), ('3rd Term', 'third term')], help_text='Select subject term', max_length=30, null=True),
        ),
    ]
