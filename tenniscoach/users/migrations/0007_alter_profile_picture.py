# Generated by Django 5.0.6 on 2024-06-24 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, default='media/static/images/unknown_user.jpg', upload_to='static/users_pics'),
        ),
    ]
