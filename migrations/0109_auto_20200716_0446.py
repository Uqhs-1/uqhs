# Generated by Django 2.1.3 on 2020-07-16 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0108_auto_20200708_0516'),
    ]

    operations = [
        migrations.AddField(
            model_name='qsubject',
            name='annual_avg',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2020-07-16', max_length=200),
        ),
        migrations.AlterField(
            model_name='downloadformat',
            name='created',
            field=models.DateTimeField(default='2020-07-16', max_length=200),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='agn',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='agr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='annual_scores',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='atd',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='exam',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='test',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='registered_id',
            name='student_name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_id', to='result.CNAME'),
        ),
    ]
