# Generated by Django 2.2.4 on 2019-09-03 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mastertests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
