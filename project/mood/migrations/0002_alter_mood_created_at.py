# Generated by Django 4.2.4 on 2024-01-21 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mood',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
