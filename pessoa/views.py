from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import ListView
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Pessoa

import json 

def validate_post_body(body):
    if not body['apelido'] or not body['nome'] or not body['nascimento']:
        return False
    if type(body['apelido']) is not str or not len(body['apelido']) or len(body['apelido']) > 32:
        return False
    if type(body['nome']) is not str or not len(body['nome']) or len(body['apelido']) > 100:
        return False
    if type(body['nascimento']) is not str or not len(body['nascimento']) or len(body['nascimento']) != 10:
        return False
    
    ano, mes, dia = body['nascimento'].split('-')
    if int(ano) < 1:
        return False
    if int(mes) < 1 or int(mes)> 12:
        return False
    if int(dia) < 1 or int(dia) > 31:
        return False
    
    if body['stack']:
        for tech in body['stack']:
            if type(tech) is not str or len(tech) > 32:
                return False 

    return True
    
class PessoaContagemView(ListView):
    def get(self, request):
        return HttpResponse(Pessoa.objects.count())
    
class PessoaView(ListView):
    def get(self, request, pessoa_id=None):
        if pessoa_id is None:
            t = request.GET.get('t', None)
            if not t:
                return HttpResponse(status=400)
            pessoas = Pessoa.objects.filter(
                Q(apelido__icontains=t)|
                Q(nome__icontains=t)|
                Q(stack__icontains=t)
            ).values('id', 'apelido', 'nome', 'nascimento', 'stack')
            return JsonResponse(list(pessoas), safe=False)

        pessoa = get_object_or_404(Pessoa, id=pessoa_id)

        data = {
            'id': str(pessoa.id),
            'apelido': pessoa.apelido,
            'nome': pessoa.nome,
            'nascimento': pessoa.nascimento.isoformat(),
            'stack': pessoa.stack,
        }
        return JsonResponse(data)
        
    def post(self, request):
        data = json.loads(request.body)
        valid_json = validate_post_body(data)
        if not valid_json:
            return HttpResponse(status=400)
        pessoa = Pessoa(
            apelido=data['apelido'],
            nome=data['nome'],
            nascimento=data['nascimento'],
            stack=data['stack'],
        )
        try:
            pessoa.save()
            return HttpResponse(status=201,headers={"Location": f"/pessoas/{pessoa.pk}"})
        except IntegrityError as e:
            return HttpResponse(status=422)
