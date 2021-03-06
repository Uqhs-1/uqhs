# Generated by Django 2.1.3 on 2020-04-14 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0085_auto_20200410_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='STUDENT_INFO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(default='2019/JS_1/10', max_length=200, null=True)),
                ('no_open', models.IntegerField(blank=True, default=122, null=True)),
                ('no_present', models.IntegerField(blank=True, default=122, null=True)),
                ('no_absent', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.CharField(default='Satisfactory', max_length=200, null=True)),
                ('H_begin', models.IntegerField(blank=True, default=1.76, null=True)),
                ('H_end', models.IntegerField(blank=True, default=1.78, null=True)),
                ('W_begin', models.IntegerField(blank=True, default=60.76, null=True)),
                ('W_end', models.IntegerField(blank=True, default=60.78, null=True)),
                ('no_of_day_abs', models.IntegerField(blank=True, default=0, null=True)),
                ('purpose', models.CharField(default='Not Specified', max_length=200, null=True)),
                ('good', models.CharField(default='Good', max_length=200, null=True)),
                ('fair', models.CharField(default='Fair', max_length=200, null=True)),
                ('poor', models.CharField(default='Poor', max_length=200, null=True)),
                ('remark', models.CharField(default='Good keep it up', max_length=200, null=True)),
                ('event', models.CharField(default='______', max_length=200, null=True)),
                ('indoor', models.CharField(default='______', max_length=200, null=True)),
                ('ball', models.CharField(default='_____', max_length=200, null=True)),
                ('combat', models.CharField(default='_____', max_length=200, null=True)),
                ('track', models.CharField(default='______', max_length=200, null=True)),
                ('jump', models.CharField(default='______', max_length=200, null=True)),
                ('throw', models.CharField(default='______', max_length=200, null=True)),
                ('swim', models.CharField(default='_____', max_length=200, null=True)),
                ('lift', models.CharField(default='_____', max_length=200, null=True)),
                ('sport_comment', models.CharField(default='Satisfactory', max_length=200, null=True)),
                ('club_one', models.CharField(default='MSSN', max_length=200, null=True)),
                ('club_two', models.CharField(default='JET', max_length=200, null=True)),
                ('office_one', models.CharField(default='Mosque Coordinator.', max_length=200, null=True)),
                ('office_two', models.CharField(default='Time keeper', max_length=200, null=True)),
                ('contrib_one', models.CharField(default='Proper arrangement of School mosque', max_length=200, null=True)),
                ('contrib_two', models.CharField(default='Manage program timely', max_length=200, null=True)),
                ('student_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='result.CNAME')),
            ],
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2020-04-14', max_length=200),
        ),
        migrations.AlterField(
            model_name='downloadformat',
            name='created',
            field=models.DateTimeField(default='2020-04-14', max_length=200),
        ),
        migrations.AddField(
            model_name='qsubject',
            name='info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='result.STUDENT_INFO'),
        ),
    ]
