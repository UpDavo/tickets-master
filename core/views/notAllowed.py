from django.shortcuts import render


def NotAllowed(request):
    return render(request, 'errors/not_allowed.html')
