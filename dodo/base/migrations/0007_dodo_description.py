# Generated by Django 5.0.2 on 2024-04-17 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_rename_name_dodo_user_dodo_dodo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dodo',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
