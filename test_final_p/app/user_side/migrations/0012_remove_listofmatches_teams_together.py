# Generated by Django 4.0.2 on 2022-05-17 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0011_alter_listofmatches_home_team_result_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listofmatches',
            name='teams_together',
        ),
    ]
