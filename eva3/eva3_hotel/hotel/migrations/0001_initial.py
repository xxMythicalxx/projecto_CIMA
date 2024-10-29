# Generated by Django 4.1.2 on 2022-11-29 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomcroom', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomsize', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.TextField(max_length=15)),
                ('pas', models.TextField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('description', models.TextField(max_length=50)),
                ('Nhotel', models.TextField(max_length=50)),
                ('type', models.TextField(max_length=50)),
                ('price', models.TextField(max_length=50)),
                ('Nbathroom', models.TextField(max_length=50)),
                ('Nroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.nroom')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.size')),
            ],
        ),
        migrations.CreateModel(
            name='His',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('des', models.TextField(max_length=200)),
                ('tableinfo', models.TextField(max_length=100)),
                ('hour', models.DateTimeField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.usuario')),
            ],
        ),
    ]