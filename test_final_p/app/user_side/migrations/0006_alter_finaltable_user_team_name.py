# Generated by Django 4.0.2 on 2022-05-15 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0005_alter_allteams_team_id_alter_allusers_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finaltable',
            name='user_team_name',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
