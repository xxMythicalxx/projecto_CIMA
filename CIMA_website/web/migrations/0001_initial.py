# Generated by Django 4.0 on 2024-10-31 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.TextField(max_length=15)),
                ('nombres', models.TextField(max_length=30)),
                ('lastnombre', models.TextField(max_length=30)),
                ('curso', models.TextField(max_length=20)),
                ('salon', models.TextField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.TextField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Estado_Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.TextField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='His',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.TextField(max_length=20)),
                ('descripcion', models.TextField(max_length=200)),
                ('tableinfo', models.TextField(max_length=100)),
                ('hour', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.TextField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.TextField(max_length=15)),
                ('password', models.TextField(max_length=20)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.tipo_usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(max_length=15)),
                ('descripcion', models.TextField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('razon_ingreso', models.TextField(choices=[('comprado', 'comprado'), ('donado', 'donado')], max_length=20)),
                ('estado_habil', models.TextField(choices=[('activo', 'activo'), ('desactivo', 'desactivo')], max_length=20)),
                ('fecha_ingreso', models.DateTimeField()),
                ('fecha_egreso', models.DateTimeField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.categoria')),
                ('estado_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.estado_producto')),
                ('rut_alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.alumno')),
            ],
        ),
    ]
