# Generated by Django 4.0.2 on 2022-05-15 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0006_alter_finaltable_user_team_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='finaltable',
            old_name='user_achive_guru_tutu',
            new_name='user_achive_guru_turu',
        ),
        migrations.AlterField(
            model_name='finaltable',
            name='user_position',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]