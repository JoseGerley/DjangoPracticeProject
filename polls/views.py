from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Estas en la pagina principal de Premios Platzi App.")


def detail(request, question_id):
    return HttpResponse(f"Estas viendo la pregunta número {question_id}.")


def results(request, question_id):
    return HttpResponse(f"Estas viendo los resultados de la pregunta número {question_id}.")

def vote(request, question_id):
    return HttpResponse(f"Estas votando en la pregunta número {question_id}.")