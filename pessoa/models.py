from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
class Pessoa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,null=False)
    apelido = models.CharField(max_length=32,unique=True)
    nome = models.CharField(max_length=100) 
    nascimento = models.DateField()
    stack = ArrayField(models.CharField(max_length=32, blank=False), null=True)