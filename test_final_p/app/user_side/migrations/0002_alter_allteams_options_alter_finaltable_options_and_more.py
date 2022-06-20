# Generated by Django 4.0.2 on 2022-06-18 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_side', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allteams',
            options={'verbose_name': 'Команди (учасників)', 'verbose_name_plural': 'Команди (учасників)'},
        ),
        migrations.AlterModelOptions(
            name='finaltable',
            options={'verbose_name': 'Підсумкова таблиця', 'verbose_name_plural': 'Підсумкова таблиця'},
        ),
        migrations.AlterModelOptions(
            name='listofmatches',
            options={'verbose_name': 'Список матчів', 'verbose_name_plural': 'Список матчів'},
        ),
        migrations.AlterModelOptions(
            name='listofusersmatchforecast',
            options={'verbose_name': 'Прогнози всіх учасників', 'verbose_name_plural': 'Прогнози всіх учасників'},
        ),
        migrations.RemoveField(
            model_name='listofusersmatchforecast',
            name='users',
        ),
        migrations.AlterField(
            model_name='finaltable',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_fintable', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='finaltable',
            name='user_team_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team_choices', to='user_side.allteams'),
        ),
        migrations.AlterField(
            model_name='listofusersmatchforecast',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_forecasts', to=settings.AUTH_USER_MODEL),
        ),
    ]
