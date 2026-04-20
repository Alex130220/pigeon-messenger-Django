from django.urls import path
from . import views

app_name = 'messenger'
urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('send/', views.send_message, name='send_message'),
    path('select-user/', views.select_user, name='select_user'),
    path('inbox/', views.inbox, name='inbox'),
    path('chat/', views.conversation_list, name='chat'),
    path('conversations/', views.conversation_list, name='conversation_list'),  # Добавили новый
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
]
