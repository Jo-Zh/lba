# Generated by Django 4.0.5 on 2022-06-17 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_description_posts_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='set_public',
            field=models.BooleanField(default=False),
        ),
    ]
