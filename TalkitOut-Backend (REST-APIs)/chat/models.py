from django.db import models
from django.utils import timezone

# Create your models here.
# #! model for chatroom
# class ChatRoom(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=200)
#     #! to string method
#     def __str__(self):
#         return self.name
    
# #! model for message
# class Message(models.Model):
#     chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
#     message = models.CharField(max_length=200)
#     #! to string method
#     def __str__(self):
#         return self.message
    
# #! model for user
# class User(models.Model):
#     name = models.CharField(max_length=100)
#     #! to string method
#     def __str__(self):
#         return self.name

# #! model for user in chatroom
# class UserInChatRoom(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
#     #! to string method
#     def __str__(self):
#         return self.user.name + " in " + self.chatroom.name

from django.db import models

# Create your models here.
class ChatMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    chatroom_name = models.CharField(max_length=255)
    sender_username = models.CharField(max_length=255)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    time = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.message_id}: {self.sender_username} in {self.chatroom_name}: {self.message_content}'
    
    def is_expired(self):
        if self.time is None:
            return False  # Message set to be retained forever
        expiration_time = self.timestamp + timezone.timedelta(seconds=self.time)
        if timezone.now() > expiration_time:
            self.message_content = '[SCHEDULED DELETE]'
            self.save()
            return True
        else:
            return False