# Generated by Django 4.2.21 on 2025-05-23 00:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('savings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengeProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_index', models.PositiveIntegerField()),
                ('is_saved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserChallenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_amount', models.PositiveIntegerField()),
                ('total_units', models.PositiveIntegerField()),
                ('unit', models.CharField(choices=[('week', '주'), ('month', '월')], max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('started_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='savingcheck',
            name='challenge',
        ),
        migrations.AddField(
            model_name='challengetemplate',
            name='default_goal_amount',
            field=models.PositiveIntegerField(default=100000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='challengetemplate',
            name='default_total_units',
            field=models.PositiveIntegerField(default=100000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='challengetemplate',
            name='default_unit',
            field=models.CharField(choices=[('week', '주'), ('month', '월')], default='week', max_length=10),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='SavingChallenge',
        ),
        migrations.DeleteModel(
            name='SavingCheck',
        ),
        migrations.AddField(
            model_name='userchallenge',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='savings.challengetemplate'),
        ),
        migrations.AddField(
            model_name='userchallenge',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='challengeprogress',
            name='user_challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progresses', to='savings.userchallenge'),
        ),
        migrations.AlterUniqueTogether(
            name='challengeprogress',
            unique_together={('user_challenge', 'unit_index')},
        ),
    ]
