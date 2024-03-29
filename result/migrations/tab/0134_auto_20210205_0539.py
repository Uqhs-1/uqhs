# Generated by Django 2.2.13 on 2021-02-05 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0133_auto_20200911_1735'),
    ]

    operations = [    
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2021-02-05', max_length=200),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='subject',
            field=models.CharField(blank=True, choices=[('----', 'None'), ('ACC', 'Account'), ('AGR', 'Agric. Sc.'), ('ARB', 'Arabic'), ('BST', 'Basic Science and Technology'), ('BIO', 'Biology'), ('BUS', 'Business Studies'), ('CTR', 'Catering'), ('CHE', 'Chemistry'), ('CIV', 'Civic Education'), ('COM', 'Commerce'), ('ECO', 'Economics'), ('ELE', 'Electrical'), ('ENG', 'English'), ('FUR', 'Furthe Mathematics'), ('GRM', 'Garment Making'), ('GEO', 'Geography'), ('GOV', 'Government'), ('HIS', 'History'), ('ICT', 'Information Technology'), ('IRS', 'Islamic Studies'), ('LIT', 'Litrature'), ('MAT', 'Mathematics'), ('NAV', 'National Value'), ('PHY', 'Physics'), ('PRV', 'Pre-Vocation'), ('YOR', 'Yoruba')], default='ENG', help_text='select subject NAME', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='cname',
            name='contrib_one',
            field=models.CharField(blank=True, default='Active member', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cname',
            name='contrib_two',
            field=models.CharField(blank=True, default='Active member', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cname',
            name='office_one',
            field=models.CharField(blank=True, default='Member', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cname',
            name='office_two',
            field=models.CharField(blank=True, default='Member', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='edit_user',
            name='class_in',
            field=models.CharField(blank=True, choices=[('JSS 1', 'ONE'), ('JSS 2', 'TWO'), ('JSS 3', 'THREE'), ('SSS 1', 'FOUR'), ('SSS 2', 'FIVE'), ('SSS 3', 'SIX'), ('HEADS', 'HOD')], default=None, help_text='Select class in charge', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='edit_user',
            name='resumption',
            field=models.DateField(blank=True, default='2021-02-05', help_text='Date format: MM/DD/YYYY', null=True),
        ),
    ]
