# Generated by Django 4.0.4 on 2022-05-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='complement',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
