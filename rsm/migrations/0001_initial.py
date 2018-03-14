# Generated by Django 2.0 on 2017-12-11 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostName', models.CharField(max_length=20, null=True)),
                ('hostIP', models.GenericIPAddressField()),
                ('hostUser', models.CharField(max_length=10, null=True)),
                ('hostPort', models.CharField(max_length=5, null=True)),
            ],
        ),
    ]
