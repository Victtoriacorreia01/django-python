from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Serviço
import re
from django.core import serializers
import json


def clientes(request):
        if request.method == "GET":
                clientes_list = Cliente.objects.all()
                return render(request, 'clientes.html', {'clientes': clientes_list})
        elif request.method == "POST":
                nome = request.POST.get('nome')
                sobrenome = request.POST.get('sobrenome')
                email = request.POST.get('email')
                cpf = request.POST.get('cpf')
                serviço = request.POST.getlist('serviço')
                func = request.POST.getlist('func')
                data = request.POST.getlist('data')

                cliente = Cliente.objects.filter(cpf=cpf)

                if cliente.exists():
                        return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'carros': zip(serviço, func, data) })

                if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
                        return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(serviço, func, data)})


                cliente = Cliente(
                        nome = nome,
                        sobrenome = sobrenome,
                        email = email,
                        cpf = cpf
                )

                cliente.save()
                
                for serviço, func, data in zip(serviço, func, data):
                        serv = Serviço(serviço=serviço, func=func, data=data, cliente=cliente)
                        serv.save()
                
                return HttpResponse('Teste')
        
def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    serviços = Serviço.objects.filter(cliente=cliente[0])
    cliente = Cliente.objects.filter(id=id_cliente)
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    return JsonResponse(cliente_json)
