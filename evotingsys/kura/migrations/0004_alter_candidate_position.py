# Generated by Django 4.1.5 on 2023-02-17 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kura', '0003_alter_candidate_year_of_study'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='Position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kura.position'),
        ),
    ]
