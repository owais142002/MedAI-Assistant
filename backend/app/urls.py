from django.urls import path
from . import views
from app.controller.loginController import signup, validate_user
from app.controller.aiController import query, clearChatHistory

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('validate_user/', validate_user, name='validate_user'),
    path('chat/', query, name="chat"),
    path('clear_chat/', clearChatHistory, name="clear_chat"),
]