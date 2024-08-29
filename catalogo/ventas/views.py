import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import redirect, render

from .models import Foto, Producto, Referencia


# Create your views here.
def custom_logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def ver_referencias(request):
    grupos_desc = Referencia.objects.values_list("grupo_desc", flat=True).distinct()
    busqueda = request.GET.get("busqueda", "")
    color = request.GET.get("color", "")
    subgrupo = request.GET.get("subgrupo", "")
    colores = (
        Producto.objects.filter(cantidad__gte=0)
        .values_list("color", flat=True)
        .distinct()
    )
    subgrupos = []

    # Filtrar las referencias en base a la descripción del grupo
    if busqueda:
        subgrupos = (
            Referencia.objects.filter(
                fotos__isnull=False,
                descripcion__icontains=busqueda,
            )
            .values_list("subgrupo", "subgrupo_desc")
            .distinct()
        )
        if color and subgrupo:
            referencias = Referencia.objects.filter(
                fotos__isnull=False,
                descripcion__icontains=busqueda,
                productos__color=color,
                subgrupo=subgrupo,
            ).distinct()
        elif color:
            referencias = Referencia.objects.filter(
                fotos__isnull=False,
                descripcion__icontains=busqueda,
                productos__color=color,
            ).distinct()
        elif subgrupo:
            referencias = Referencia.objects.filter(
                fotos__isnull=False,
                descripcion__icontains=busqueda,
                subgrupo=subgrupo,
            ).distinct()
        else:
            referencias = Referencia.objects.filter(
                fotos__isnull=False, descripcion__icontains=busqueda
            ).distinct()
    else:
        referencias = (
            Referencia.objects.filter(fotos__isnull=False)
            .order_by("-id")
            .distinct()[:20]
        )
    return render(
        request,
        "referencias.html",
        {
            "referencias": referencias,
            "grupos_desc": grupos_desc,
            "busqueda": busqueda,
            "colores": colores,
            "subgrupos": subgrupos,
        },
    )


@login_required
def check_referencia_photos(request):
    grupos_desc = Referencia.objects.values_list("grupo_desc", flat=True).distinct()
    lista = []
    if request.method == "POST":
        referencias = Referencia.objects.filter(fotos__isnull=True).distinct()
        for referencia in referencias:
            diccionario = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f"}
            # Suponiendo que tienes una URL para verificar las fotos
            for i in range(1, 6):  # Por ejemplo, verificando hasta 5 fotos
                letra = diccionario[i]
                foto_url = f"http://201.236.231.148/fotosVtex/todas/{referencia.codigo}{referencia.consecutivo}{referencia.codcolor}_{letra}.jpg"
                response = requests.get(foto_url)
                if response.status_code == 200:
                    # Guarda la foto en el modelo
                    foto = Foto(referencia=referencia)
                    foto.imagen.save(
                        f"{referencia.codigo}{referencia.consecutivo}{referencia.codcolor}_{letra}.jpg",
                        ContentFile(response.content),
                    )
                    foto.save()
                else:
                    if i == 1:
                        lista.append(
                            f"{referencia.codigo}{referencia.consecutivo}{referencia.codcolor} no se hallo imagen."
                        )

    return render(request, "subir.html", {"lista": lista, "grupos_desc": grupos_desc})
