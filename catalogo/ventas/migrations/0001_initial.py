# Generated by Django 5.1 on 2024-08-29 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='fotos/')),
            ],
            options={
                'db_table': 'catalogo_ventas_foto',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('talla', models.CharField(max_length=10)),
                ('codcolor', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=300)),
                ('cantidad', models.IntegerField()),
            ],
            options={
                'db_table': 'catalogo_ventas_producto',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Referencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100)),
                ('consecutivo', models.IntegerField()),
                ('codcolor', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200)),
                ('grupo', models.CharField(max_length=300)),
                ('subgrupo', models.CharField(max_length=300)),
                ('grupo_desc', models.CharField(max_length=300)),
                ('subgrupo_desc', models.CharField(max_length=300)),
                ('coleccion', models.CharField(max_length=300)),
                ('composicion', models.CharField(max_length=300)),
                ('mayor', models.CharField(max_length=300)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'catalogo_ventas_referencia',
                'managed': False,
            },
        ),
    ]
