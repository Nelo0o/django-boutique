# Generated by Django 5.2.4 on 2025-07-25 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commandes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('nouvelle_commande', 'Nouvelle commande'), ('stock_faible', 'Stock faible'), ('info', 'Information')], default='info', max_length=20)),
                ('titre', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('lu', models.BooleanField(default=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('commande', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commandes.commande')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ['-date_creation'],
            },
        ),
    ]
