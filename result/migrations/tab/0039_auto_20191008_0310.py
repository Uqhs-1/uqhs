# Generated by Django 2.1.3 on 2019-10-07 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0038_auto_20191001_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asubjects',
            name='name',
            field=models.CharField(blank=True, choices=[('ACC', 'Account'), ('AGR', 'Agric. Sc.'), ('ARB', 'Arabic'), ('BST', 'Basic Science and Technology'), ('BIO', 'Biology'), ('BUS', 'Business Studies'), ('CTR', 'Catering'), ('CHE', 'Chemistry'), ('CIV', 'Civic Education'), ('COM', 'Commerce'), ('ECO', 'Economics'), ('ELE', 'Electrical'), ('ENG', 'English'), ('FUR', 'Furthe Mathematics'), ('GRM', 'Garment Making'), ('GEO', 'Geography'), ('GOV', 'Government'), ('HIS', 'History'), ('ICT', 'Information Technology'), ('IRS', 'Islamic Studies'), ('LIT', 'Litrature'), ('MAT', 'Mathematics'), ('NAV', 'National Value'), ('PHY', 'Physics'), ('PRV', 'Pre-Vocation'), ('YOR', 'Yoruba'), ('None', None)], default='English', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2019-10-08', max_length=200),
        ),
        migrations.AlterField(
            model_name='session',
            name='created',
            field=models.DateTimeField(default='2019-10-08', max_length=200),
        ),
    ]