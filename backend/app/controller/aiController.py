from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.http import JsonResponse, StreamingHttpResponse
from adrf.decorators import api_view
import json
from channels.db import database_sync_to_async
import app.agents.routerAgent as MainAgentService
from django.views.decorators.csrf import csrf_exempt
from app.utils import safe_access_event, to_serializable_format
import asyncio
import nest_asyncio
from django.http.response import StreamingHttpResponse


@api_view(["POST"])
async def query(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Authentication credentials were not provided.'}, status=401)
    
    token = auth_header.split(' ')[1]
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(token)
        user = await database_sync_to_async(jwt_auth.get_user)(validated_token)
        user_id = user.id
    except AuthenticationFailed:
        return JsonResponse({'error': 'Invalid token or expired token.'}, status=401)
    
    data = json.loads(request.body)   
    query = data.get("query")
    fibbit_access_token = data.get("fitbit_access_token", '')
    image_url = data.get("image_url",'')

    agent = MainAgentService.createRouterAgent(user_id)
    memory = MainAgentService.getMemory(user_id)
    chat_history = memory.buffer_as_messages

    async def data_generator():
        async for event in agent.astream_events(
            {"input": query, "chat_history": chat_history},
            {"tags": [user_id, query, fibbit_access_token, image_url]},
            version="v1",
        ):
            stream_type = event["event"]
            if stream_type == "on_chat_model_stream" and safe_access_event(
                event, ["data", "chunk"]
            ):
                if event["data"]["chunk"].content.strip(" \t\r") != "":
                    yield str(event["data"]["chunk"].content)

    return StreamingHttpResponse(data_generator(), status=200)


@api_view(["GET"])
def clearChatHistory(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Authentication credentials were not provided.'}, status=401)
    
    token = auth_header.split(' ')[1]
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(token)
        user = jwt_auth.get_user(validated_token)
        user_id = user.id
    except AuthenticationFailed:
        return JsonResponse({'error': 'Invalid token or expired token.'}, status=401)    
    
    memory = MainAgentService.getMemory(user_id)
    memory.clear()    

    return JsonResponse({'status': 'memory cleared successfully.'}, status=200)
    

@api_view(["GET"])
def getChatHistory(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Authentication credentials were not provided.'}, status=401)
    
    token = auth_header.split(' ')[1]
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(token)
        user = jwt_auth.get_user(validated_token)
        user_id = user.id
    except AuthenticationFailed:
        return JsonResponse({'error': 'Invalid token or expired token.'}, status=401)    
    
    memory = MainAgentService.getMemory(user_id)
    chat_history = memory.buffer_as_messages
    chat_history_serialized = to_serializable_format(chat_history)

    return JsonResponse({'data':chat_history_serialized }, status=200)
    