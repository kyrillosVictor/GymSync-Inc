# Generated by Django 4.2.15 on 2024-09-10 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_alter_trainermessage_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainermessage',
            name='user_type',
        ),
    ]
