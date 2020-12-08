from django.shortcuts import render
from .models import Medicamento

# Create your views here.
def cadastro_medicamentos(request):
    droga = Medicamento.objects.values_list("principio_ativo", flat=True)
    droga_list = list()
    for i in droga:
        droga_list.append(i)
    if request.method == "POST":
        p = request.POST
        item = Medicamento(
            nome_medicamento = p.get("name"),
            classificacao = p.get("classificacao"), 
            principio_ativo =p.get("principio_ativo")
            )
        item.save()
        print(item.nome_medicamento)


    return render(request,'pagina_cadastro_medicamento.html',{"droga":droga_list})

