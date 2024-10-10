from django.db import models
from django.contrib.postgres.fields import ArrayField
class Pessoa(models.Model):
    apelido = models.CharField(max_length=32,unique=True)
    nome = models.CharField(max_length=100) 
    nascimento = models.DateField()
    stack = ArrayField(models.CharField(max_length=32, blank=False), null=True)