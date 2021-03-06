# Generated by Django 2.1.3 on 2019-08-18 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ANNUAL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(blank=True, max_length=40, null=True)),
                ('anual', models.FloatField(blank=True, max_length=10, null=True)),
                ('Agr', models.FloatField(blank=True, max_length=10, null=True)),
                ('Grade', models.CharField(blank=True, max_length=5, null=True)),
                ('Posi', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'ordering': ('student_name_id',),
            },
        ),
        migrations.CreateModel(
            name='ASUBJECTS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('English', 'English'), ('Mathematics', 'Mathematics'), ('Civic Education', 'Civic Education'), ('Electrical', 'Electrical'), ('Yoruba', 'Yoruba'), ('Agric. Sc.', 'Agric. Sc.'), ('Garment Making', 'Garment Making'), ('Pre-Vocation', 'Pre-Vocation'), ('Information Technology', 'Information Technology'), ('Biology', 'Biology'), ('Chemistry', 'Chemistry'), ('Physics', 'Physics'), ('Geography', 'Geography'), ('Government', 'Government'), ('Account', 'Account'), ('Arabic', 'Arabic'), ('Islamic Studies', 'Islamic Studies'), ('Litrature', 'Litrature'), ('Commerce', 'Commerce'), ('Economics', 'Economics'), ('Business Studies', 'Business Studies'), ('Basic Science and Technology', 'Basic Science and Technology'), ('Catering', 'Catering'), ('National Value', 'National Value'), ('Furthe Mathematics', 'Furthe Mathematics'), ('History', 'History')], default='English', max_length=30, null=True)),
                ('model_in', models.CharField(blank=True, default='subject', max_length=8, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='BTUTOR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(blank=True, help_text='Subject Teacher', max_length=50, null=True)),
                ('Class', models.CharField(blank=True, choices=[('JSS 1', 'jss_one'), ('JSS 2', 'jss_two'), ('JSS 3', 'jss_three'), ('SS 1', 'sss_one'), ('SS 2', 'sss_two'), ('SS 3', 'sss_three')], help_text='Select subject class', max_length=30, null=True)),
                ('term', models.CharField(blank=True, choices=[('1st Term', 'first term'), ('2nd Term', 'second term'), ('3rd Term', 'third term')], help_text='Select subject term', max_length=30, null=True)),
                ('model_summary', models.CharField(blank=True, default='tutor', max_length=1000, null=True)),
                ('model_in', models.CharField(blank=True, default='qsubject', max_length=8, null=True)),
                ('males', models.IntegerField(blank=True, default='0', help_text='Enter number of male in class', null=True)),
                ('females', models.IntegerField(blank=True, default='0', help_text='Enter number of female in class', null=True)),
                ('cader', models.CharField(blank=True, help_text='Senior/Junior', max_length=1, null=True)),
                ('session', models.CharField(blank=True, help_text='Must be 4 didits {2016}', max_length=5, null=True)),
                ('class_teacher_id', models.CharField(blank=True, help_text='Class teacher id', max_length=200, null=True)),
                ('created', models.DateTimeField(default='2019-08-19', max_length=200)),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('accounts', models.ForeignKey(blank=True, help_text='loggon-account:move account here', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='btutor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CNAME',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(blank=True, max_length=30, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('subject_code', models.IntegerField(blank=True, default='0', null=True)),
                ('model_summary', models.CharField(blank=True, default='student_names', max_length=200, null=True)),
                ('Class', models.CharField(blank=True, choices=[('JSS 1', 'jss_one'), ('JSS 2', 'jss_two'), ('JSS 3', 'jss_three'), ('SS 1', 'sss_one'), ('SS 2', 'sss_two'), ('SS 3', 'sss_three')], max_length=30, null=True)),
            ],
            options={
                'ordering': ('student_name',),
            },
        ),
        migrations.CreateModel(
            name='Edit_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Mr.', 'Mr'), ('Mrs.', 'Mrs'), ('Sir.', 'Senior officer'), ('Ma.', 'Madam'), ('Mall.', 'Mallam'), ('Ust.', 'Ustadh'), ('Alh.', 'Alhaj'), ('Dr.', 'Doctor'), ('Engr.', 'Engineer')], default='Mr.', help_text='Select title to address you.', max_length=15, null=True)),
                ('last_name', models.CharField(help_text='(Surname)-Required', max_length=20, null=True)),
                ('first_name', models.CharField(help_text='(Other names)-Required', max_length=20, null=True)),
                ('photo', models.ImageField(null=True, upload_to='static/result/images/')),
                ('image', models.CharField(blank=True, max_length=30, null=True)),
                ('bio', models.TextField(blank=True, default='I am a professional science teacher, currently working with the aboved named School. If you plan on changing the font face and its color only once on a web page, you need to change its attributes in the element tag. Using the style attribute, you may specify the font face and color with font-family, color, and the font size with font-size, as shown in the example below.', help_text='Your summarised biography')),
                ('phone', models.CharField(blank=True, help_text='Hotline', max_length=20)),
                ('city', models.CharField(blank=True, default='Ibadan', help_text='Your town in the state of origin', max_length=15)),
                ('country', models.CharField(blank=True, default='Nigeria', help_text='Nationality', max_length=10)),
                ('organization', models.CharField(blank=True, default='IIRO', help_text='Oganization affliated with', max_length=10)),
                ('location', models.CharField(blank=True, help_text='Current location', max_length=30)),
                ('birth_date', models.DateField(blank=True, help_text='Date format: MM/DD/YYYY', null=True)),
                ('department', models.CharField(blank=True, choices=[('Sc', 'Sciences'), ('SSc', 'Social Sciences'), ('Art', 'Arts and Humanities')], max_length=30, null=True)),
                ('account_id', models.CharField(blank=True, default=0, max_length=30, null=True)),
                ('email_confirmed', models.BooleanField(default=False, help_text='True/False')),
                ('class_in', models.CharField(blank=True, choices=[('JSS 1', 'jss_one'), ('JSS 2', 'jss_two'), ('JSS 3', 'jss_three'), ('SS 1', 'sss_one'), ('SS 2', 'sss_two'), ('SS 3', 'sss_three')], default=None, help_text='Select class in charge', max_length=15, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('account_id',),
            },
        ),
        migrations.CreateModel(
            name='OVERALL_ANNUAL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_in', models.CharField(blank=True, choices=[('JSS 1', 'jss_one'), ('JSS 2', 'jss_two'), ('JSS 3', 'jss_three'), ('SS 1', 'sss_one'), ('SS 2', 'sss_two'), ('SS 3', 'sss_three')], max_length=30, null=True)),
                ('AGR', models.FloatField(blank=True, default='0', max_length=8, null=True)),
                ('AVR', models.FloatField(blank=True, default='0', max_length=8, null=True)),
                ('GRD', models.CharField(blank=True, default='0', max_length=8, null=True)),
                ('POS', models.CharField(blank=True, default='0', max_length=8, null=True)),
                ('session', models.CharField(blank=True, help_text='Must be 4 didits {2016}', max_length=5, null=True)),
                ('acc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='acc', to='result.ANNUAL')),
                ('agr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agr', to='result.ANNUAL')),
                ('bst', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bst', to='result.ANNUAL')),
                ('bus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bus', to='result.ANNUAL')),
                ('eng', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eng', to='result.ANNUAL')),
                ('his', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='his', to='result.ANNUAL')),
                ('ict', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arb', to='result.ANNUAL')),
                ('irs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='irs', to='result.ANNUAL')),
                ('mat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mat', to='result.ANNUAL')),
                ('nva', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nva', to='result.ANNUAL')),
                ('prv', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prv', to='result.ANNUAL')),
                ('student_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='result.CNAME')),
                ('teacher_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='all_subject', to=settings.AUTH_USER_MODEL)),
                ('yor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='yor', to='result.ANNUAL')),
            ],
            options={
                'ordering': ('class_in',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(max_length=1000)),
                ('Account_Username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QSUBJECT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.FloatField(blank=True, max_length=4, null=True)),
                ('agn', models.FloatField(blank=True, max_length=4, null=True)),
                ('atd', models.FloatField(blank=True, max_length=4, null=True)),
                ('total', models.FloatField(blank=True, max_length=4, null=True)),
                ('exam', models.FloatField(blank=True, max_length=4, null=True)),
                ('agr', models.FloatField(blank=True, max_length=4, null=True)),
                ('grade', models.CharField(blank=True, max_length=5, null=True)),
                ('posi', models.CharField(blank=True, max_length=5, null=True)),
                ('gender', models.CharField(blank=True, help_text='sex', max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('cader', models.CharField(blank=True, choices=[('s', 'Senior'), ('j', 'Junior')], max_length=1, null=True)),
                ('model_in', models.CharField(blank=True, default='qsubject', max_length=8, null=True)),
                ('annual_scores', models.CharField(blank=True, max_length=100, null=True)),
                ('Class', models.CharField(blank=True, choices=[('JSS 1', 'jss_one'), ('JSS 2', 'jss_two'), ('JSS 3', 'jss_three'), ('SS 1', 'sss_one'), ('SS 2', 'sss_two'), ('SS 3', 'sss_three')], max_length=30, null=True)),
                ('logged_in', models.ForeignKey(blank=True, help_text='subject_teacher', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logins', to=settings.AUTH_USER_MODEL)),
                ('student_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='result.CNAME')),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='result.BTUTOR')),
            ],
            options={
                'ordering': ('student_name_id',),
            },
        ),
        migrations.CreateModel(
            name='RESULT_GRADE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.IntegerField(blank=True, default='0', null=True)),
                ('model_in', models.CharField(blank=True, default='grades', max_length=6, null=True)),
                ('subject', models.CharField(blank=True, choices=[('English', 'English'), ('Mathematics', 'Mathematics'), ('Civic Education', 'Civic Education'), ('Electrical', 'Electrical'), ('Yoruba', 'Yoruba'), ('Agric. Sc.', 'Agric. Sc.'), ('Garment Making', 'Garment Making'), ('Pre-Vocation', 'Pre-Vocation'), ('Information Technology', 'Information Technology'), ('Biology', 'Biology'), ('Chemistry', 'Chemistry'), ('Physics', 'Physics'), ('Geography', 'Geography'), ('Government', 'Government'), ('Account', 'Account'), ('Arabic', 'Arabic'), ('Islamic Studies', 'Islamic Studies'), ('Litrature', 'Litrature'), ('Commerce', 'Commerce'), ('Economics', 'Economics'), ('Business Studies', 'Business Studies'), ('Basic Science and Technology', 'Basic Science and Technology'), ('Catering', 'Catering'), ('National Value', 'National Value'), ('Furthe Mathematics', 'Furthe Mathematics'), ('History', 'History')], default='BroadSheet', max_length=30, null=True)),
                ('grade_A', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_C', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_P', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_F', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_A1', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_B2', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_B3', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_C4', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_C5', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_C6', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_D7', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_E8', models.IntegerField(blank=True, default='0', null=True)),
                ('grade_F9', models.IntegerField(blank=True, default='0', null=True)),
                ('remark', models.BooleanField(default=False, help_text='True/False')),
            ],
            options={
                'ordering': ('subject',),
            },
        ),
        migrations.CreateModel(
            name='SESSION',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new', models.CharField(blank=True, choices=[('2019', '2018/2019'), ('2020', '2019/2020'), ('2021', '2020/2021'), ('2022', '2021/2022'), ('2023', '2022/2023'), ('2024', '2023/2024'), ('2025', '2024/2025'), ('2026', '2025/2026'), ('2027', '2026/2027'), ('2028', '2027/2028'), ('2029', '2028/2029'), ('2030', '2029/2030'), ('2031', '2030/2031'), ('2032', '2031/2032'), ('2033', '2032/2033'), ('2034', '2033/2034'), ('2035', '2034/2035'), ('2036', '2035/2036'), ('2037', '2036/2037'), ('2038', '2037/2038'), ('2039', '2038/2039'), ('2040', '2039/2040'), ('2041', '2040/2041'), ('2042', '2041/2042'), ('2043', '2042/2043'), ('2044', '2043/2044'), ('2045', '2044/2045'), ('2046', '2045/2046'), ('2047', '2046/2047'), ('2048', '2047/2048')], default='2019', max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'session',
                'verbose_name_plural': 'sessions',
                'db_table': 'school_session',
            },
        ),
        migrations.AddField(
            model_name='btutor',
            name='graded',
            field=models.ForeignKey(blank=True, help_text='Grade Counts', null=True, on_delete=django.db.models.deletion.CASCADE, to='result.RESULT_GRADE'),
        ),
        migrations.AddField(
            model_name='btutor',
            name='subject',
            field=models.ForeignKey(blank=True, help_text='Select subject', null=True, on_delete=django.db.models.deletion.SET_NULL, to='result.ASUBJECTS'),
        ),
        migrations.AddField(
            model_name='btutor',
            name='teacher_in',
            field=models.ForeignKey(blank=True, help_text='Class Teachers', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_account', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='annual',
            name='first',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annual_first', to='result.QSUBJECT'),
        ),
        migrations.AddField(
            model_name='annual',
            name='second',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annual_second', to='result.QSUBJECT'),
        ),
        migrations.AddField(
            model_name='annual',
            name='student_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='result.CNAME'),
        ),
        migrations.AddField(
            model_name='annual',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='result.ASUBJECTS'),
        ),
        migrations.AddField(
            model_name='annual',
            name='subject_by',
            field=models.ForeignKey(blank=True, help_text='subject_teacher', null=True, on_delete=django.db.models.deletion.CASCADE, to='result.BTUTOR'),
        ),
        migrations.AddField(
            model_name='annual',
            name='third',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annual_third', to='result.QSUBJECT'),
        ),
    ]
