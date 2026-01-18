from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

@login_required
def index(request):
    """Vista principal del dashboard protegida por autenticación"""
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard/dashboard.html', context)