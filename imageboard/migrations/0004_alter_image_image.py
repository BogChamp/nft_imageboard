# Generated by Django 3.2.12 on 2022-03-01 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageboard', '0003_auto_20220301_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
