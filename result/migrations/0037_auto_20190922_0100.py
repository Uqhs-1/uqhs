# Generated by Django 2.1.3 on 2019-09-21 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0036_auto_20190913_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annual',
            name='student_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='result.CNAME'),
        ),
        migrations.AlterField(
            model_name='annual',
            name='third',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='third', to='result.QSUBJECT'),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2019-09-22', max_length=200),
        ),
        migrations.AlterField(
            model_name='overall_annual',
            name='student_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='result.CNAME'),
        ),
        migrations.AlterField(
            model_name='overall_annual',
            name='teacher_in',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='all_subject', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='qsubject',
            name='student_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='result.CNAME'),
        ),
        migrations.AlterField(
            model_name='session',
            name='created',
            field=models.DateTimeField(default='2019-09-22', max_length=200),
        ),
    ]
