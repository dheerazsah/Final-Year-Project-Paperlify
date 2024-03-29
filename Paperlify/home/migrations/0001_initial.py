# Generated by Django 4.2.4 on 2023-09-25 12:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('fname', models.CharField(default='none', max_length=100)),
                ('email', models.EmailField(default='none', max_length=254, unique=True)),
                ('password', models.CharField(default='none', max_length=128)),
                ('updatedOn', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
