from django.shortcuts import render


def home(request):
    return render(request, "api/home.html")


def must(request):
    return render(request, "api/must.html")


def game(request):
    return render(request, "api/game.html")
