# Generated by Django 4.0.5 on 2022-06-29 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='发送时间'),
        ),
    ]
