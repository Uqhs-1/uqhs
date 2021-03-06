# Generated by Django 2.1.3 on 2020-04-18 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0093_auto_20200417_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2020-04-18', max_length=200),
        ),
        migrations.AlterField(
            model_name='downloadformat',
            name='created',
            field=models.DateTimeField(default='2020-04-18', max_length=200),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='ball',
            field=models.CharField(blank=True, default='_____', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='club_one',
            field=models.CharField(blank=True, default='MSSN', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='club_two',
            field=models.CharField(blank=True, default='JET', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='combat',
            field=models.CharField(blank=True, default='_____', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='comment',
            field=models.CharField(blank=True, default='Satisfactory', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='contrib_one',
            field=models.CharField(blank=True, default='Proper arrangement of School mosque', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='contrib_two',
            field=models.CharField(blank=True, default='Manage program timely', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='event',
            field=models.CharField(blank=True, default='______', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='fair',
            field=models.CharField(blank=True, default='None', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='good',
            field=models.CharField(blank=True, default='None', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='indoor',
            field=models.CharField(blank=True, default='______', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='jump',
            field=models.CharField(blank=True, default='______', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='lift',
            field=models.CharField(blank=True, default='_____', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='office_one',
            field=models.CharField(blank=True, default='Mosque Coordinator.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='office_two',
            field=models.CharField(blank=True, default='Time keeper', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='poor',
            field=models.CharField(blank=True, default='None', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='remark',
            field=models.CharField(blank=True, default='Good keep it up', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='sport_comment',
            field=models.CharField(blank=True, default='Satisfactory', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='swim',
            field=models.CharField(blank=True, default='_____', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='throw',
            field=models.CharField(blank=True, default='______', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='student_info',
            name='track',
            field=models.CharField(blank=True, default='______', max_length=10, null=True),
        ),
    ]
