# Generated by Django 5.2.4 on 2025-07-22 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='es_admin',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='telefono',
        ),
        migrations.AddField(
            model_name='perfil',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatares/'),
        ),
        migrations.AddField(
            model_name='perfil',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
