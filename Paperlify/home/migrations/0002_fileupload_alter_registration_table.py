# Generated by Django 4.2.4 on 2023-09-29 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AlterModelTable(
            name='registration',
            table=None,
        ),
    ]
