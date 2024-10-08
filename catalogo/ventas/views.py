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


def ver_referencias(request):
    # Obtener parámetros de búsqueda
    busqueda = request.GET.get("busqueda", "")
    color = request.GET.get("color", "")
    subgrupo = request.GET.get("subgrupo", "")

    # Consulta base
    referencias = Referencia.objects.filter(
        fotos__isnull=False, productos__cantidad__gt=0
    ).distinct()

    # Aplicar filtros
    if busqueda:
        referencias = referencias.filter(grupo_desc__icontains=busqueda)
    if color:
        referencias = referencias.filter(productos__color=color)
    if subgrupo:
        referencias = referencias.filter(subgrupo=subgrupo)

    # Limitar a 20 resultados si no hay filtros
    if not (busqueda or color or subgrupo):
        referencias = referencias.order_by("-id")[:20]

    # Obtener datos para los selects
    grupos_desc = (
        Referencia.objects.values_list("grupo_desc", flat=True)
        .distinct()
        .order_by("grupo_desc")
    )
    colores = (
        Producto.objects.filter(cantidad__gte=0)
        .values_list("color", flat=True)
        .distinct()
    )
    subgrupos = (
        Referencia.objects.filter(fotos__isnull=False)
        .values_list("subgrupo", "subgrupo_desc")
        .distinct()
    )

    # Si hay búsqueda, filtrar subgrupos
    if busqueda:
        subgrupos = subgrupos.filter(grupo_desc__icontains=busqueda)

    context = {
        "referencias": referencias,
        "grupos_desc": grupos_desc,
        "busqueda": busqueda,
        "colores": colores,
        "subgrupos": subgrupos,
    }

    return render(request, "referencias.html", context)


@login_required
def check_referencia_photos(request):

    lista = []
    if request.method == "POST":
        referencias = Referencia.objects.filter(
            fotos__isnull=True, productos__cantidad__gte=0
        ).distinct()
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
                        foto_url = f"http://201.236.231.148/fotosVtex/todas/{referencia.codigo}{referencia.codcolor}_{letra}.png"
                        response = requests.get(foto_url)
                        if response.status_code == 200:
                            # Guarda la foto en el modelo
                            foto = Foto(referencia=referencia)
                            foto.imagen.save(
                                f"{referencia.codigo}{referencia.codcolor}_{letra}.png",
                                ContentFile(response.content),
                            )
                            foto.save()
                        else:
                            lista.append(
                                f"{referencia.codigo}{referencia.consecutivo}{referencia.codcolor} no se hallo imagen."
                            )

    return render(request, "subir.html", {"lista": lista})
