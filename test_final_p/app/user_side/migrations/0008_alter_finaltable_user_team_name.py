# Generated by Django 4.0.2 on 2022-06-18 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0007_alter_finaltable_user_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finaltable',
            name='user_team_name',
            field=models.ForeignKey(blank=True, db_constraint=False, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_side.allteams'),
        ),
    ]
