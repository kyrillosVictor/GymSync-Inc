# Generated by Django 4.2.15 on 2024-09-08 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_alter_trainersalary_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='email',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='full_name',
            field=models.TextField(max_length=100),
        ),
    ]
