# Generated by Django 2.1.3 on 2019-10-07 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0051_auto_20191008_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asubjects',
            name='name',
            field=models.CharField(blank=True, choices=[('ACC', 'Account'), ('AGR', 'Agric. Sc.'), ('ARB', 'Arabic'), ('BST', 'Basic Science and Technology'), ('BIO', 'Biology'), ('BUS', 'Business Studies'), ('CTR', 'Catering'), ('CHE', 'Chemistry'), ('CIV', 'Civic Education'), ('COM', 'Commerce'), ('ECO', 'Economics'), ('ELE', 'Electrical'), ('ENG', 'English'), ('FUR', 'Furthe Mathematics'), ('GRM', 'Garment Making'), ('GEO', 'Geography'), ('GOV', 'Government'), ('HIS', 'History'), ('ICT', 'Information Technology'), ('IRS', 'Islamic Studies'), ('LIT', 'Litrature'), ('MAT', 'Mathematics'), ('NAV', 'National Value'), ('PHY', 'Physics'), ('PRV', 'Pre-Vocation'), ('YOR', 'Yoruba')], default='ENG', help_text='select subject NAME', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='Class',
            field=models.CharField(choices=[('JSS 1', 'jss_one'), ('JSS 2', 'jss_two'), ('JSS 3', 'jss_three'), ('SSS 1', 'sss_one'), ('SSS 2', 'sss_two'), ('SSS 3', 'sss_three')], default='JSS 1', help_text='select subject CLASS', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='subject',
            field=models.ForeignKey(help_text='select subject NAME', null=True, on_delete=django.db.models.deletion.CASCADE, to='result.ASUBJECTS'),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='term',
            field=models.CharField(blank=True, choices=[('1st Term', 'first term'), ('2nd Term', 'second term'), ('3rd Term', 'third term')], default='1st Term', help_text='select subject TERM', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='new',
            field=models.CharField(choices=[('2019', '2018/2019'), ('2020', '2019/2020'), ('2021', '2020/2021'), ('2022', '2021/2022'), ('2023', '2022/2023'), ('2024', '2023/2024'), ('2025', '2024/2025'), ('2026', '2025/2026'), ('2027', '2026/2027'), ('2028', '2027/2028'), ('2029', '2028/2029'), ('2030', '2029/2030'), ('2031', '2030/2031'), ('2032', '2031/2032'), ('2033', '2032/2033'), ('2034', '2033/2034'), ('2035', '2034/2035'), ('2036', '2035/2036'), ('2037', '2036/2037'), ('2038', '2037/2038'), ('2039', '2038/2039'), ('2040', '2039/2040'), ('2041', '2040/2041'), ('2042', '2041/2042'), ('2043', '2042/2043'), ('2044', '2043/2044'), ('2045', '2044/2045'), ('2046', '2045/2046'), ('2047', '2046/2047'), ('2048', '2047/2048')], default='2019', help_text='select academic SESSION', max_length=30, null=True),
        ),
    ]
