# Generated by Django 4.2.5 on 2023-11-30 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_f_animal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='f_animal',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
