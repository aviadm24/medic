# Generated by Django 3.1 on 2021-01-18 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
