# Generated by Django 4.0.2 on 2022-06-30 17:55

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('send_reminder', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Зареєстровані Користувачі',
                'verbose_name_plural': 'Зареєстровані Користувачі',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AllTeams',
            fields=[
                ('team_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Team ID')),
                ('team_name', models.CharField(max_length=25)),
                ('team_points', models.PositiveIntegerField(blank=True, default=0)),
                ('team_position', models.PositiveIntegerField(blank=True, default=0)),
            ],
            options={
                'verbose_name': 'Команди (учасників)',
                'verbose_name_plural': 'Команди (учасників)',
            },
        ),
        migrations.CreateModel(
            name='ListOfMatches',
            fields=[
                ('match_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Match ID')),
                ('round_number', models.PositiveIntegerField(default=1)),
                ('match_in_round', models.PositiveIntegerField(default=1)),
                ('home_team', models.CharField(default='', max_length=20)),
                ('visitor_team', models.CharField(default='', max_length=20)),
                ('teams_together', models.CharField(default='', max_length=41)),
                ('match_date', models.DateField()),
                ('match_time', models.TimeField()),
                ('forecast_availability', models.CharField(default='no', max_length=3)),
                ('home_team_result', models.PositiveIntegerField(blank=True, null=True)),
                ('visitor_team_result', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Список матчів',
                'verbose_name_plural': 'Список матчів',
            },
        ),
        migrations.CreateModel(
            name='ListOfUsersMatchForecast',
            fields=[
                ('forecast_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Forecast ID')),
                ('teams_together', models.CharField(default='', max_length=41)),
                ('home_team_forecast', models.PositiveIntegerField()),
                ('visitor_team_forecast', models.PositiveIntegerField()),
                ('round_number', models.PositiveIntegerField(default=1)),
                ('forecast_time', models.DateTimeField(auto_now_add=True)),
                ('user_points', models.PositiveIntegerField(blank=True, null=True)),
                ('forecast_type', models.CharField(max_length=9)),
                ('match_in_round', models.PositiveIntegerField(default=1)),
                ('match_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_side.listofmatches')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_forecasts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Прогнози всіх учасників',
                'verbose_name_plural': 'Прогнози всіх учасників',
            },
        ),
        migrations.CreateModel(
            name='FinalTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=25)),
                ('user_position', models.PositiveIntegerField(blank=True, default=0)),
                ('user_points', models.PositiveIntegerField(default=0)),
                ('user_potential_points', models.PositiveIntegerField(default=0)),
                ('user_average_point_per_match', models.FloatField(default=0.0)),
                ('user_all_predicted_matches', models.PositiveIntegerField(default=0)),
                ('user_predicted_match_score', models.PositiveIntegerField(default=0)),
                ('user_predicted_match_result', models.PositiveIntegerField(default=0)),
                ('user_predicted_express', models.PositiveIntegerField(default=0)),
                ('user_not_predicted_express', models.PositiveIntegerField(default=0)),
                ('user_achive_guru_turu', models.PositiveIntegerField(default=0)),
                ('user_team_name', models.CharField(blank=True, choices=[], max_length=225)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_fintable', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Підсумкова таблиця',
                'verbose_name_plural': 'Підсумкова таблиця',
            },
        ),
    ]