# Generated by Django 4.0.2 on 2022-05-17 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0013_alter_listofmatches_home_team_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listofmatches',
            name='teams_together',
            field=models.CharField(default='', max_length=41),
        ),
    ]