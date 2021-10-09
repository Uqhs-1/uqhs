# Generated by Django 2.1.3 on 2020-07-29 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0114_auto_20200722_2052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cname',
            options={'ordering': ('full_name',)},
        ),
        migrations.AddField(
            model_name='edit_user',
            name='resumption',
            field=models.CharField(blank=True, default='Monday January 9, 2017.', max_length=115, null=True),
        ),
        migrations.AddField(
            model_name='edit_user',
            name='session',
            field=models.CharField(choices=[('2019', '2018/2019'), ('2020', '2019/2020'), ('2021', '2020/2021'), ('2022', '2021/2022'), ('2023', '2022/2023'), ('2024', '2023/2024'), ('2025', '2024/2025'), ('2026', '2025/2026'), ('2027', '2026/2027'), ('2028', '2027/2028'), ('2029', '2028/2029'), ('2030', '2029/2030'), ('2031', '2030/2031'), ('2032', '2031/2032'), ('2033', '2032/2033'), ('2034', '2033/2034'), ('2035', '2034/2035'), ('2036', '2035/2036'), ('2037', '2036/2037'), ('2038', '2037/2038'), ('2039', '2038/2039'), ('2040', '2039/2040'), ('2041', '2040/2041'), ('2042', '2041/2042'), ('2043', '2042/2043'), ('2044', '2043/2044'), ('2045', '2044/2045'), ('2046', '2045/2046'), ('2047', '2046/2047'), ('2048', '2047/2048')], default='2019', help_text='select academic SESSION', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='btutor',
            name='created',
            field=models.DateTimeField(default='2020-07-29', max_length=200),
        ),
        migrations.AlterField(
            model_name='downloadformat',
            name='created',
            field=models.DateTimeField(default='2020-07-29', max_length=200),
        ),
    ]