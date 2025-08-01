from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


@require_http_methods(["DELETE"])
@login_required
def delete_user(request):
    """
    View to delete the currently logged-in user and trigger cleanup of related data.
    """
    user = request.user
    username = user.username
    user.delete()
    return JsonResponse({'message': f'User {username} deleted successfully.'}, status=200)
