# Generated by Django 4.2.6 on 2023-10-27 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_subjectmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectmodel',
            name='createat',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
