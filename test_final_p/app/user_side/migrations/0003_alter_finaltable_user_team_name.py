# Generated by Django 4.0.2 on 2022-06-18 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0002_alter_allteams_options_alter_finaltable_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finaltable',
            name='user_team_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='team_choices', to='user_side.allteams'),
        ),
    ]
