# Generated by Django 2.1.3 on 2019-12-24 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0065_auto_20191224_1504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='question',
            name='serial_no',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]