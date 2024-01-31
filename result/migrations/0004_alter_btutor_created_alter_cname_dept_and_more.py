# Generated by Django 5.0.1 on 2024-01-24 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0003_rename_annual_scores_cname_total_scores_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2024-01-24', max_length=200),
        ),
        migrations.AlterField(
            model_name='cname',
            name='dept',
            field=models.CharField(blank=True, default='nill', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='cname',
            name='grade',
            field=models.CharField(blank=True, default='D7', max_length=115, null=True),
        ),
        migrations.AlterField(
            model_name='cname',
            name='no',
            field=models.IntegerField(blank=True, default=0, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='cname',
            name='posi',
            field=models.CharField(blank=True, default='th', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='edit_user',
            name='resumption',
            field=models.DateField(blank=True, default='2024-01-24', help_text='Date format: MM/DD/YYYY', null=True),
        ),
    ]
