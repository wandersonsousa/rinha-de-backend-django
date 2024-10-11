from django.urls import path

from .views import PessoaView

urlpatterns = [
    path("", PessoaView.as_view()),
    path("<uuid:pessoa_id>/", PessoaView.as_view()),
]
