from django.shortcuts import render


def marketplace(request, id=None):
    return render(request, 'marketplace.html')
