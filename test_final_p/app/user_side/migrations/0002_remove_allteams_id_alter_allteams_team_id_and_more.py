# Generated by Django 4.0.2 on 2022-05-05 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allteams',
            name='id',
        ),
        migrations.AlterField(
            model_name='allteams',
            name='team_id',
            field=models.PositiveIntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='allteams',
            name='team_points',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='allteams',
            name='team_position',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
