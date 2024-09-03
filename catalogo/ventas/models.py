from django.db import models


# Create your models here.
class Referencia(models.Model):
    codigo = models.CharField(max_length=100)
    consecutivo = models.IntegerField()
    codcolor = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    grupo = models.CharField(max_length=300)
    subgrupo = models.CharField(max_length=300)
    grupo_desc = models.CharField(max_length=300)
    subgrupo_desc = models.CharField(max_length=300)
    coleccion = models.CharField(max_length=300)
    composicion = models.CharField(max_length=300)
    mayor = models.CharField(max_length=300)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_mayorista = models.IntegerField()
    descuento_tiquete = models.IntegerField()
    diseno = models.CharField(max_length=300)
    molde = models.CharField(max_length=300)

    @property
    def precio_mayor_con_descuento(self):
        return ((100 - self.descuento_mayorista) / 100) * int(self.mayor)

    @property
    def precio_tiquete_con_descuento(self):
        return ((100 - self.descuento_tiquete) / 100) * int(self.precio)

    def __str__(self):
        return self.codigo

    class Meta:
        db_table = "catalogo_ventas_referencia"
        managed = False


class Producto(models.Model):
    referencia = models.ForeignKey(
        Referencia, on_delete=models.CASCADE, related_name="productos"
    )
    codigo = models.CharField(max_length=100)
    talla = models.CharField(max_length=10)
    codcolor = models.CharField(max_length=100)
    color = models.CharField(max_length=300)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.referencia.codigo + " " + self.talla + " " + self.color

    class Meta:
        db_table = "catalogo_ventas_producto"
        managed = False


class Foto(models.Model):
    referencia = models.ForeignKey(
        Referencia, related_name="fotos", on_delete=models.CASCADE, null=True
    )
    imagen = models.ImageField(upload_to="fotos/")

    class Meta:
        db_table = "catalogo_ventas_foto"
        managed = False
