# Generated by Django 4.2.15 on 2024-08-20 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_remove_subplanfeature_subplan_subplanfeature_subplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplan',
            name='max_member',
            field=models.IntegerField(null=True),
        ),
    ]
