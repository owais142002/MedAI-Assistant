from django.urls import path
from . import views
from app.controller.loginController import signup, validate_user
from app.controller.aiController import query, clearChatHistory, getChatHistory

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('validate-user/', validate_user, name='validate-user'),
    path('chat/', query, name="chat"),
    path('clear-chat/', clearChatHistory, name="clear-chat"),
    path('chat-history/', getChatHistory, name="chat-history")    

]