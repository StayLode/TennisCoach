# Generated by Django 5.0.6 on 2024-06-14 08:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('essential', '0002_course_user_alter_profile_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essential.profile'),
        ),
    ]
