from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def puntuacions(request):
    return render(request, 'joc/puntuacions.html')
