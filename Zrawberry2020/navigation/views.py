from django.shortcuts import render


def navigation_index(request):
    return render(request, "navigation/nav_index.html")