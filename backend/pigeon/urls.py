"""
URL configuration for pigeon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from two_factor.urls import urlpatterns as tf_urls
from .views import (
    home_view,
    about_view,
    features_view,
    CustomLoginView,
    RegisterView,
    profile,
    user_dashboard,
    get_messages,
    handler404,
    handler500,
    health_check
)
import messenger.routing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('features/', features_view, name='features'),
    
    # Аутентификация (оставлен только CustomLoginView)
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', require_POST(LogoutView.as_view()), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # Сброс пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Профиль и dashboard
    path('profile/', profile, name='profile'),
    path('dashboard/', user_dashboard, name='dashboard'),
    
    # API и messenger
    path('api/', include('messenger.api.urls')),
    path('api/messages/', get_messages, name='get_messages'),
    path('messenger/', include('messenger.urls')),
    
    # Дополнительные маршруты
    path('users/', include('users.urls')),
    path('account/', include(tf_urls)),
    path('health/', health_check, name='health_check'),
    
    # WebSocket маршруты (обновлены для работы с conversation_id)
    re_path(r'^ws/conversation/(?P<conversation_id>\w+)/$', AuthMiddlewareStack(
        URLRouter(
            messenger.routing.websocket_urlpatterns
        )
    )),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pigeon.views.handler404'
handler500 = 'pigeon.views.handler500'

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            messenger.routing.websocket_urlpatterns
        )
    ),
})
