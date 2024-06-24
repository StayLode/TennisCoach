# Generated by Django 5.0.6 on 2024-06-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_purchases'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='description',
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, default='/static/images/unknown_user.jpg', upload_to='static/users_pics'),
        ),
    ]
