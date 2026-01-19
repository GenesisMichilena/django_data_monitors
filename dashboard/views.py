from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.conf import settings
import requests

@login_required
@permission_required('dashboard.index_viewer', raise_exception=True)
def index(request):
    total_responses = 0
    try:
        response = requests.get(settings.API_URL, timeout=5)
        response.raise_for_status()
        posts = response.json()
        total_responses = len(posts) if isinstance(posts, list) else 0
    except Exception:
        total_responses = 0

    context = {
        'title': "Landing Page' Dashboard",
        'total_responses': total_responses,
    }
    return render(request, 'dashboard/index.html', context)

def custom_permission_denied(request, exception=None):
    return render(request, '403.html', {'user': request.user}, status=403)
