from django.shortcuts import render


def v404_view(request, exception=None, ):
    return render(request, '404.html')