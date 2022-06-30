# Generated by Django 4.0.5 on 2022-06-29 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='name',
            field=models.CharField(default='-', max_length=155),
        ),
        migrations.AlterField(
            model_name='comments',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.comments'),
        ),
    ]