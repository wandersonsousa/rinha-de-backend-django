# Generated by Django 5.1.2 on 2024-10-10 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0007_alter_pessoa_stack'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='apelido',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]