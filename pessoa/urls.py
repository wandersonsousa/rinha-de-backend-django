from django.urls import path

from . import views

urlpatterns = [
    path("", views.PessoaView.as_view()),
]