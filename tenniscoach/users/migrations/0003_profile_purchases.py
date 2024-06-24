# Generated by Django 5.0.6 on 2024-06-23 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essential', '0013_alter_course_picture_alter_purchase_utente'),
        ('users', '0002_alter_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='purchases',
            field=models.ManyToManyField(blank=True, through='essential.Purchase', to='essential.course'),
        ),
    ]
