# Generated by Django 2.1.3 on 2020-07-29 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0123_edit_user_resumption'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annual',
            name='first',
        ),
        migrations.RemoveField(
            model_name='annual',
            name='second',
        ),
        migrations.RemoveField(
            model_name='annual',
            name='student_name',
        ),
        migrations.RemoveField(
            model_name='annual',
            name='subject_by',
        ),
        migrations.RemoveField(
            model_name='annual',
            name='third',
        ),
        migrations.DeleteModel(
            name='DOWNLOADFORMAT',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='acc',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='agr',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='bst',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='bus',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='eng',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='his',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='ict',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='irs',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='mat',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='nva',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='prv',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='student_name',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='teacher_in',
        ),
        migrations.RemoveField(
            model_name='overall_annual',
            name='yor',
        ),
        migrations.RemoveField(
            model_name='registered_id',
            name='student_name',
        ),
        migrations.DeleteModel(
            name='SESSION',
        ),
        migrations.RemoveField(
            model_name='student_info',
            name='student_name',
        ),
        migrations.DeleteModel(
            name='ANNUAL',
        ),
        migrations.DeleteModel(
            name='OVERALL_ANNUAL',
        ),
        migrations.DeleteModel(
            name='REGISTERED_ID',
        ),
        migrations.DeleteModel(
            name='STUDENT_INFO',
        ),
    ]
