from django.shortcuts import render


def Error404(request, exception):
    return render(request, 'errors/404.html', {}, status=404)
