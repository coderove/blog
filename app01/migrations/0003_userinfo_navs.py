# Generated by Django 4.0.5 on 2022-06-24 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_articles_pwd_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='navs',
            field=models.ManyToManyField(blank=True, to='app01.navs', verbose_name='收藏的网站'),
        ),
    ]
