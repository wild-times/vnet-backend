# Generated by Django 3.2.14 on 2022-07-05 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='coreuser',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='coreuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile/images/def/pc.jpg', null=True, upload_to='profiles/images/pc/'),
        ),
    ]