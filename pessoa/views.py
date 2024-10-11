from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from django.db import IntegrityError

from .models import Pessoa

import json 

def validate_post_body(body):
    if not body['apelido'] or not body['nome'] or not body['nascimento']:
        print('Missing field')
        return False
    if type(body['apelido']) is not str or not len(body['apelido']) or len(body['apelido']) > 32:
        print('field apelido')
        return False
    if type(body['nome']) is not str or not len(body['nome']) or len(body['apelido']) > 100:
        print('field nome')
        return False
    if type(body['nascimento']) is not str or not len(body['nascimento']) or len(body['nascimento']) != 10:
        print('field nascimento')
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
    

class PessoaView(ListView):
    def get(self, request, pessoa_id):
        pessoa = Pessoa.objects.get(pessoa_id)
        
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
            print('e', e)
            return HttpResponse(status=422)
