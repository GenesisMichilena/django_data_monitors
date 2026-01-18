from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

@login_required
@permission_required('dashboard.index_viewer', raise_exception=True)
def index(request):
    """Vista principal del dashboard protegida por autenticación Y permisos"""
    context = {
        'user': request.user,
        'permissions': list(request.user.get_all_permissions()),
        'has_index_permission': request.user.has_perm('dashboard.index_viewer'),
    }
    return render(request, 'dashboard/dashboard.html', context)

def custom_permission_denied(request, exception=None):
    """Vista personalizada para errores 403 - GUÍA 26"""
    return render(request, '403.html', {'user': request.user}, status=403)
