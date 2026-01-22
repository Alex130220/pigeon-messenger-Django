from django.db import models
from django.conf import settings

# Используем AUTH_USER_MODEL из настроек
User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # Убрана запятая в конце этой строки
        null=True,  
        blank=True
    )  # Закрывающая скобка была не на месте
    message = models.TextField()
    notification_type = models.CharField(max_length=20)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_message = models.ForeignKey(
        'messenger.Message', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
