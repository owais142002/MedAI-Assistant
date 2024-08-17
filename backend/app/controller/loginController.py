from django.contrib.auth import authenticate, login
from app.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
import json
from adrf.decorators import api_view

@api_view(["POST"])  
@csrf_exempt
def signup(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=201)

@api_view(["POST"])    
@csrf_exempt
def validate_user(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return JsonResponse({
            'message': 'User authenticated successfully',
            'user_id': user.id,
            'access_token': access_token,
            'refresh_token': refresh_token,
        }, status=200)
    else:
        return JsonResponse({'error': 'Invalid username or password'}, status=400)
