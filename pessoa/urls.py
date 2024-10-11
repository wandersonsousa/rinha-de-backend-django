from django.urls import path

from . import views

urlpatterns = [
    path("", views.PessoaView.as_view()),
    path("<uuid:pessoa_id>/", views.PessoaView.as_view()),
    path("contagem-pessoas/", views.PessoaContagemView.as_view())
]
