# Generated by Django 2.1.3 on 2019-10-18 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0055_auto_20191019_0449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor_home',
            name='first_term',
            field=models.ForeignKey(blank=True, default='0', help_text='Not editable', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first', to='result.BTUTOR'),
        ),
        migrations.AlterField(
            model_name='tutor_home',
            name='second_term',
            field=models.ForeignKey(blank=True, default='0', help_text='Not editable', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second', to='result.BTUTOR'),
        ),
        migrations.AlterField(
            model_name='tutor_home',
            name='third_term',
            field=models.ForeignKey(blank=True, default='0', help_text='Not editable', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third', to='result.BTUTOR'),
        ),
    ]
