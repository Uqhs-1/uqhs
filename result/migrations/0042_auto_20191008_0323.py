# Generated by Django 2.1.3 on 2019-10-07 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0041_auto_20191008_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asubjects',
            name='name',
            field=models.CharField(blank=True, choices=[('ACC', 'Account'), ('AGR', 'Agric. Sc.'), ('ARB', 'Arabic'), ('BST', 'Basic Science and Technology'), ('BIO', 'Biology'), ('BUS', 'Business Studies'), ('CTR', 'Catering'), ('CHE', 'Chemistry'), ('CIV', 'Civic Education'), ('COM', 'Commerce'), ('ECO', 'Economics'), ('ELE', 'Electrical'), ('ENG', 'English'), ('FUR', 'Furthe Mathematics'), ('GRM', 'Garment Making'), ('GEO', 'Geography'), ('GOV', 'Government'), ('HIS', 'History'), ('ICT', 'Information Technology'), ('IRS', 'Islamic Studies'), ('LIT', 'Litrature'), ('MAT', 'Mathematics'), ('NAV', 'National Value'), ('PHY', 'Physics'), ('PRV', 'Pre-Vocation'), ('YOR', 'Yoruba'), (None, 'All')], default='English', max_length=30, null=True),
        ),
    ]
