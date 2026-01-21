from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import JsonResponse
from users.forms import CustomUserCreationForm
from messenger.models import Message, ChatRoom
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from messenger.serializers import MessageSerializer

class CustomLoginView(LoginView):
    """Кастомное представление для входа"""
    template_name = 'users/login.html'

class RegisterView(CreateView):
    """Представление для регистрации пользователя"""
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Обработка успешной регистрации"""
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Регистрация прошла успешно!')
        return super().form_valid(form)

def home_view(request):
    """Главная страница"""
    if request.user.is_authenticated:
        recent_messages = Message.objects.filter(
            recipient=request.user
        ).select_related('sender').order_by('-timestamp')[:5]
        return render(request, 'home.html', {
            'recent_messages': recent_messages
        })
    return render(request, 'home.html')

def about_view(request):
    """Страница 'О нас'"""
    return render(request, 'about.html', {
        'team_members': [
            {'name': 'Александр', 'role': 'Разработчик'},
            {'name': 'Команда', 'role': 'Дизайнеры'}
        ]
    })

def features_view(request):
    """Страница 'Возможности'"""
    features = [
        "Обмен текстовыми сообщениями",
        "Групповые чаты",
        "Шифрование сообщений",
        "История переписки",
        "Уведомления в реальном времени"
    ]
    return render(request, 'features.html', {'features': features})

@login_required
def profile(request):
    """Профиль пользователя"""
    return render(request, 'users/profile.html')

@login_required
def user_dashboard(request):
    """Личный кабинет пользователя"""
    user = request.user
    unread_count = Message.objects.filter(
        recipient=user,
        is_read=False
    ).count()
    
    return render(request, 'users/dashboard.html', {
        'unread_count': unread_count,
        'active_chats': ChatRoom.objects.filter(members=user)[:5]
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request):
    try:
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)

def health_check(request):
    return JsonResponse({'status': 'ok'}, status=200)
