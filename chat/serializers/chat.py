from rest_framework import (
    serializers, 
) 

from chat.models.chat import Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'