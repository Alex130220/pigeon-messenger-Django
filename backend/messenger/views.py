from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation
from django.contrib.auth import get_user_model
from .forms import MessageForm

User = get_user_model()

@login_required
def select_user(request):
    """Страница выбора пользователя для чата"""
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messenger/select_user.html', {'users': users})

@login_required
def conversation_list(request):
    """Список бесед пользователя"""
    conversations = request.user.conversations.all().order_by('-updated_at')
    return render(request, 'messenger/conversation_list.html', {
        'conversations': conversations
    })

@login_required
def start_conversation(request, user_id):
    """Создание/открытие беседы с пользователем"""
    recipient = get_object_or_404(User, id=user_id)
    
    # Ищем существующую беседу
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=recipient
    ).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, recipient)
    
    return redirect('messenger:conversation_detail', conversation_id=conversation.id)

@login_required
def conversation_detail(request, conversation_id):
    """Детали беседы с сообщениями"""
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )
    # Определяем получателя (второго участника беседы)
    recipient = conversation.participants.exclude(id=request.user.id).first()
    if not recipient:
        raise Http404("Не удалось определить получателя")
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.recipient = recipient  # Добавлено установка получателя
            message.save()
            return redirect('messenger:conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    # Помечаем сообщения как прочитанные
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    return render(request, 'messenger/conversation_detail.html', {
        'conversation': conversation,
        'form': form,  # Добавлена недостающая запятая
        'recipient': recipient
    })

@login_required
def inbox(request):
    """Контроллер для входящих сообщений"""
    # Пример реализации - показать все беседы с непрочитанными сообщениями
    conversations = request.user.conversations.filter(
        messages__is_read=False
    ).exclude(
        messages__sender=request.user
    ).distinct().order_by('-updated_at')
    
    return render(request, 'messenger/inbox.html', {
        'conversations': conversations
    })

@login_required
def chat_view(request):
    chats = Conversation.objects.filter(participants=request.user)  # Добавлено
    messages = Message.objects.filter(conversation__participants=request.user).order_by('-timestamp')[:100]
    return render(request, 'chat/chat.html', {
        'messages': messages,
        'chats': chats,
        'recipient': request.user  # Или другой получатель, если нужно
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ChatMessage.objects.create(
                user=request.user,
                message=message_text
            )
    return redirect('chat_view')
