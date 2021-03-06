# Generated by Django 2.1.3 on 2019-08-26 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0008_auto_20190825_1230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='btutor',
            options={'ordering': ('teacher_name',)},
        ),
        migrations.AlterModelOptions(
            name='cname',
            options={'ordering': ('last_name',)},
        ),
        migrations.AlterField(
            model_name='btutor',
            name='Class',
            field=models.CharField(blank=True, choices=[('JSS 1', 'jss_one'), ('JSS 2', 'jss_two'), ('JSS 3', 'jss_three'), ('SSS 1', 'sss_one'), ('SSS 2', 'sss_two'), ('SSS 3', 'sss_three')], help_text='Select subject class', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2019-08-26', max_length=200),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='Class',
            field=models.CharField(blank=True, choices=[('JSS 1', 'jss_one'), ('JSS 2', 'jss_two'), ('JSS 3', 'jss_three'), ('SSS 1', 'sss_one'), ('SSS 2', 'sss_two'), ('SSS 3', 'sss_three')], max_length=30, null=True),
        ),
    ]
