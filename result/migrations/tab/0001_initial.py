# Generated by Django 2.2.13 on 2021-07-20 21:23

from django.conf import settings
import django.core.validators
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
            name='BTUTOR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(blank=True, help_text='Subject Teacher', max_length=50, null=True)),
                ('subject', models.CharField(blank=True, choices=[('----', 'None'), ('ACC', 'Account'), ('AGR', 'Agric. Sc.'), ('ARB', 'Arabic'), ('BST', 'Basic Science and Technology'), ('BIO', 'Biology'), ('BUS', 'Business Studies'), ('CTR', 'Catering'), ('CHE', 'Chemistry'), ('CIV', 'Civic Education'), ('COM', 'Commerce'), ('ECO', 'Economics'), ('ELE', 'Electrical'), ('ENG', 'English'), ('FUR', 'Furthe Mathematics'), ('GRM', 'Garment Making'), ('GEO', 'Geography'), ('GOV', 'Government'), ('HIS', 'History'), ('ICT', 'Information Technology'), ('IRS', 'Islamic Studies'), ('LIT', 'Litrature'), ('MAT', 'Mathematics'), ('NAV', 'National Value'), ('PHY', 'Physics'), ('PRV', 'Pre-Vocation'), ('YOR', 'Yoruba')], default='ENG', help_text='select subject NAME', max_length=30, null=True)),
                ('Class', models.CharField(choices=[('JSS 1', 'jss_one'), ('JSS 2', 'jss_two'), ('JSS 3', 'jss_three'), ('SSS 1', 'sss_one'), ('SSS 2', 'sss_two'), ('SSS 3', 'sss_three')], default='JSS 1', help_text='select subject CLASS', max_length=30, null=True)),
                ('term', models.CharField(blank=True, choices=[('1st Term', 'first term'), ('2nd Term', 'second term'), ('3rd Term', 'third term')], default='1st Term', help_text='select subject TERM', max_length=30, null=True)),
                ('first_term', models.CharField(blank=True, default='1st Term', max_length=30, null=True)),
                ('second_term', models.CharField(blank=True, default='1st Term', max_length=30, null=True)),
                ('third_term', models.CharField(blank=True, default='1st Term', max_length=30, null=True)),
                ('model_summary', models.CharField(blank=True, default='tutor', max_length=1000, null=True)),
                ('model_in', models.CharField(blank=True, default='qsubject', max_length=8, null=True)),
                ('males', models.IntegerField(blank=True, default='0', help_text='Enter number of male in class', null=True)),
                ('females', models.IntegerField(blank=True, default='0', help_text='Enter number of female in class', null=True)),
                ('cader', models.CharField(blank=True, help_text='Senior/Junior', max_length=1, null=True)),
                ('status', models.CharField(blank=True, choices=[('active', 'Active'), ('delete', 'Delete')], default='active', help_text='Account Status', max_length=8, null=True)),
                ('session', models.CharField(blank=True, max_length=8, null=True)),
                ('subject_teacher_id', models.CharField(blank=True, help_text='Class teacher id', max_length=200, null=True)),
                ('created', models.DateTimeField(default='2021-07-20', max_length=200)),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('pdf', models.FileField(default='default.pdf', null=True, upload_to='static/result/pdf/')),
                ('accounts', models.ForeignKey(blank=True, help_text='loggon-account:move account here', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='btutor', to=settings.AUTH_USER_MODEL)),
                ('teacher_in', models.ForeignKey(blank=True, help_text='Class Teachers', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('teacher_name',),
            },
        ),
        migrations.CreateModel(
            name='CNAME',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(blank=True, default='Surname', max_length=30, null=True)),
                ('middle_name', models.CharField(blank=True, default='Middle nmae', max_length=30, null=True)),
                ('first_name', models.CharField(blank=True, default='First name', max_length=30, null=True)),
                ('full_name', models.CharField(blank=True, default='Surname', max_length=200, null=True)),
                ('birth_date', models.DateField(blank=True, default='2000-10-01', help_text='Date format: MM/DD/YYYY', null=True)),
                ('age', models.CharField(blank=True, default='14', max_length=30, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('gender', models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(1)])),
                ('uid', models.CharField(default='2019/JS_1/10', max_length=200, null=True)),
                ('session', models.CharField(blank=True, max_length=80, null=True)),
                ('Class', models.CharField(default='JSS 1', help_text='select subject CLASS', max_length=30, null=True)),
                ('term', models.CharField(blank=True, default='1st Term', max_length=30, null=True)),
                ('no_open', models.IntegerField(blank=True, default=122, null=True)),
                ('no_present', models.IntegerField(blank=True, default=122, null=True)),
                ('no_absent', models.IntegerField(blank=True, default=0, null=True)),
                ('contact', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.CharField(blank=True, default='Satisfactory', max_length=200, null=True)),
                ('H_begin', models.FloatField(blank=True, default=1.76, max_length=40, null=True)),
                ('H_end', models.FloatField(blank=True, default=1.78, max_length=40, null=True)),
                ('W_begin', models.FloatField(blank=True, default=60.76, max_length=40, null=True)),
                ('W_end', models.FloatField(blank=True, default=60.78, max_length=40, null=True)),
                ('no_of_day_abs', models.IntegerField(blank=True, default=0, null=True)),
                ('purpose', models.CharField(default='Not Specified', max_length=200, null=True)),
                ('good', models.CharField(blank=True, default='None', max_length=100, null=True)),
                ('fair', models.CharField(blank=True, default='None', max_length=100, null=True)),
                ('poor', models.CharField(blank=True, default='None', max_length=100, null=True)),
                ('remark', models.CharField(blank=True, default='Good keep it up', max_length=100, null=True)),
                ('event', models.CharField(blank=True, default='_____', max_length=100, null=True)),
                ('indoor', models.CharField(blank=True, default='_____', max_length=100, null=True)),
                ('ball', models.CharField(blank=True, default='_____', max_length=100, null=True)),
                ('combat', models.CharField(blank=True, default='_____', max_length=100, null=True)),
                ('track', models.CharField(blank=True, default='_____', max_length=100, null=True)),
                ('jump', models.CharField(blank=True, default='_____', max_length=100, null=True)),
                ('throw', models.CharField(blank=True, default='_____', max_length=100, null=True)),
                ('swim', models.CharField(blank=True, default='_____', max_length=100, null=True)),
                ('lift', models.CharField(blank=True, default='_____', max_length=100, null=True)),
                ('sport_comment', models.CharField(blank=True, default='Satisfactory', max_length=200, null=True)),
                ('club_one', models.CharField(blank=True, default='MSSN', max_length=200, null=True)),
                ('club_two', models.CharField(blank=True, default='JET', max_length=200, null=True)),
                ('office_one', models.CharField(blank=True, default='Member', max_length=200, null=True)),
                ('office_two', models.CharField(blank=True, default='Member', max_length=200, null=True)),
                ('contrib_one', models.CharField(blank=True, default='Active member', max_length=200, null=True)),
                ('contrib_two', models.CharField(blank=True, default='Active member', max_length=200, null=True)),
                ('sex', models.CharField(blank=True, default='Male', max_length=100, null=True)),
                ('title', models.CharField(blank=True, default='Mr/Mrs', max_length=200, null=True)),
                ('p_name', models.CharField(blank=True, default='OLAGUNJU MUSLIM', max_length=200, null=True)),
                ('occupation', models.CharField(blank=True, default='Trading', max_length=200, null=True)),
                ('contact1', models.CharField(blank=True, default='2348068302532', max_length=13, null=True)),
                ('contact2', models.CharField(blank=True, default='2348078302538', max_length=13, null=True)),
                ('address', models.CharField(blank=True, default='23, Akogun Street Olunloyo, Ibadan, Oyo State.', max_length=200, null=True)),
                ('master_comment', models.CharField(blank=True, default='He is a responsible and reliable student.', max_length=115, null=True)),
                ('principal_comment', models.CharField(blank=True, default='Fairly good performance, you can do better.', max_length=115, null=True)),
                ('resumption', models.DateTimeField(blank=True, editable=False, null=True)),
                ('annual_scores', models.IntegerField(blank=True, default=0, null=True)),
                ('annual_avr', models.FloatField(blank=True, default=0, max_length=4, null=True)),
                ('posi', models.CharField(blank=True, max_length=5, null=True)),
                ('serial_no', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'ordering': ('gender', 'Class', 'full_name'),
            },
        ),
        migrations.CreateModel(
            name='QUESTION',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjects', models.CharField(default='Undefined', max_length=200, null=True)),
                ('classes', models.CharField(default='Undefined', max_length=200, null=True)),
                ('terms', models.CharField(default='Undefined', max_length=200, null=True)),
                ('question', models.CharField(default='What is the missing question here?', max_length=1000, null=True)),
                ('optionA', models.CharField(default='Undefined', max_length=200, null=True)),
                ('answerA', models.CharField(choices=[('correct', 'Answer'), ('wrong', 'Wrong')], default='wrong', max_length=200, null=True)),
                ('optionB', models.CharField(default='Undefined', max_length=200, null=True)),
                ('answerB', models.CharField(choices=[('correct', 'Answer'), ('wrong', 'Wrong')], default='wrong', max_length=200, null=True)),
                ('optionC', models.CharField(default='Undefined', max_length=200, null=True)),
                ('answerC', models.CharField(choices=[('correct', 'Answer'), ('wrong', 'Wrong')], default='wrong', max_length=200, null=True)),
                ('optionD', models.CharField(default='Undefined', max_length=200, null=True)),
                ('answerD', models.CharField(choices=[('correct', 'Answer'), ('wrong', 'Wrong')], default='wrong', max_length=200, null=True)),
                ('CORRECT', models.CharField(default='Undefined', max_length=200, null=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, max_length=1000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('questNum', models.CharField(default='Undefined', max_length=200, null=True)),
                ('serial_no', models.IntegerField(blank=True, default=0, null=True)),
                ('photo', models.ImageField(default='Undefined', null=True, upload_to='static/result/question_image/')),
                ('image_link', models.CharField(default='default.jpg', max_length=200, null=True)),
                ('image', models.BooleanField(default=False, help_text='True/False')),
                ('session', models.CharField(blank=True, max_length=8, null=True)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='TUTOR_HOME',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(blank=True, help_text='Subject Teacher', max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('first_term', models.ForeignKey(blank=True, help_text='Not editable', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first', to='result.BTUTOR')),
                ('second_term', models.ForeignKey(blank=True, help_text='Not editable', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second', to='result.BTUTOR')),
                ('third_term', models.ForeignKey(blank=True, help_text='Not editable', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third', to='result.BTUTOR')),
                ('tutor', models.ForeignKey(blank=True, help_text='loggon-account:move account here', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_tutor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('teacher_name',),
            },
        ),
        migrations.CreateModel(
            name='QSUBJECT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(blank=True, max_length=115, null=True)),
                ('test', models.IntegerField(blank=True, default=0, null=True)),
                ('agn', models.IntegerField(blank=True, default=0, null=True)),
                ('atd', models.IntegerField(blank=True, default=0, null=True)),
                ('total', models.IntegerField(blank=True, default=0, null=True)),
                ('exam', models.IntegerField(blank=True, default=0, null=True)),
                ('agr', models.IntegerField(blank=True, default=0, null=True)),
                ('gender', models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(1)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('cader', models.CharField(blank=True, choices=[('s', 'Senior'), ('j', 'Junior')], max_length=1, null=True)),
                ('model_in', models.CharField(blank=True, default='qsubject', max_length=8, null=True)),
                ('annual_scores', models.IntegerField(blank=True, default=0, null=True)),
                ('annual_avr', models.FloatField(blank=True, default=0, max_length=4, null=True)),
                ('fagr', models.IntegerField(blank=True, default=0, null=True)),
                ('sagr', models.IntegerField(blank=True, default=0, null=True)),
                ('aagr', models.IntegerField(blank=True, default=0, null=True)),
                ('avr', models.FloatField(blank=True, max_length=4, null=True)),
                ('grade', models.CharField(blank=True, max_length=5, null=True)),
                ('posi', models.CharField(blank=True, max_length=5, null=True)),
                ('term', models.CharField(blank=True, max_length=30, null=True)),
                ('qteacher', models.CharField(blank=True, max_length=100, null=True)),
                ('logged_in', models.ForeignKey(blank=True, help_text='subject_teacher', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logins', to=settings.AUTH_USER_MODEL)),
                ('student_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='result.CNAME')),
                ('tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='result.BTUTOR')),
            ],
            options={
                'ordering': ('student_name__gender', 'student_name__full_name'),
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
            name='Edit_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Mr.', 'Mr'), ('Mrs.', 'Mrs'), ('Sir.', 'Senior officer'), ('Ma.', 'Madam'), ('Mall.', 'Mallam'), ('Ust.', 'Ustadh'), ('Alh.', 'Alhaj'), ('Dr.', 'Doctor'), ('Engr.', 'Engineer')], default='Mr.', help_text='Select title to address you.', max_length=15, null=True)),
                ('last_name', models.CharField(help_text='(Surname)-Required', max_length=20, null=True)),
                ('first_name', models.CharField(help_text='(Other names)-Required', max_length=20, null=True)),
                ('photo', models.ImageField(default='default.jpg', null=True, upload_to='static/result/images/')),
                ('image', models.CharField(blank=True, max_length=30, null=True)),
                ('bio', models.TextField(blank=True, default='I am a professional science teacher, currently working with the aboved named School. If you plan on changing the font face and its color only once on a web page, you need to change its attributes in the element tag. Using the style attribute, you may specify the font face and color with font-family, color, and the font size with font-size, as shown in the example below.', help_text='Your summarised biography')),
                ('phone', models.CharField(blank=True, help_text='Hotline', max_length=20)),
                ('city', models.CharField(blank=True, default='Ibadan', help_text='Your town in the state of origin', max_length=15)),
                ('country', models.CharField(blank=True, default='Nigeria', help_text='Nationality', max_length=10)),
                ('organization', models.CharField(blank=True, default='IIRO', help_text='Oganization affliated with', max_length=10)),
                ('location', models.CharField(blank=True, help_text='Current location', max_length=30)),
                ('birth_date', models.DateField(blank=True, help_text='Date format: MM/DD/YYYY', null=True)),
                ('department', models.CharField(blank=True, choices=[('Sc', 'Sciences'), ('SSc', 'Social Sciences'), ('Art', 'Arts and Humanities')], max_length=30, null=True)),
                ('account_id', models.CharField(blank=True, default=0, max_length=1130, null=True)),
                ('email_confirmed', models.BooleanField(default=False, help_text='True/False')),
                ('class_in', models.CharField(blank=True, choices=[('JSS 1', 'ONE'), ('JSS 2', 'TWO'), ('JSS 3', 'THREE'), ('SSS 1', 'FOUR'), ('SSS 2', 'FIVE'), ('SSS 3', 'SIX'), ('HEADS', 'HOD')], default=None, help_text='Select class in charge', max_length=15, null=True)),
                ('login_count', models.IntegerField(blank=True, default=0, null=True)),
                ('session', models.CharField(choices=[('2018', '2017/2018'), ('2019', '2018/2019'), ('2020', '2019/2020'), ('2021', '2020/2021'), ('2022', '2021/2022'), ('2023', '2022/2023'), ('2024', '2023/2024'), ('2025', '2024/2025'), ('2026', '2025/2026'), ('2027', '2026/2027'), ('2028', '2027/2028'), ('2029', '2028/2029'), ('2030', '2029/2030'), ('2031', '2030/2031'), ('2032', '2031/2032'), ('2033', '2032/2033'), ('2034', '2033/2034'), ('2035', '2034/2035'), ('2036', '2035/2036'), ('2037', '2036/2037'), ('2038', '2037/2038'), ('2039', '2038/2039'), ('2040', '2039/2040'), ('2041', '2040/2041'), ('2042', '2041/2042'), ('2043', '2042/2043'), ('2044', '2043/2044'), ('2045', '2044/2045'), ('2046', '2045/2046'), ('2047', '2046/2047'), ('2048', '2047/2048')], default='2018', help_text='select academic SESSION', max_length=30, null=True)),
                ('resumption', models.DateField(blank=True, default='2021-07-20', help_text='Date format: MM/DD/YYYY', null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('account_id',),
            },
        ),
    ]