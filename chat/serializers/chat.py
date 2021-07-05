from rest_framework import (
    serializers, 
) 

from chat.models.chat import(
    Message, GroupThread

) 

from user.serializers.user import UserPublicSerializer

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class GroupThreadSerializer(serializers.ModelSerializer):
    users = UserPublicSerializer(many=True, read_only=True)
    admins = UserPublicSerializer(many=True, read_only=True)
    created_by = UserPublicSerializer(read_only=True)

    class Meta:
        model = GroupThread
        fields = '__all__'
        
class GroupThreadDetailSerializer(serializers.ModelSerializer):
    users = UserPublicSerializer(many=True, read_only=True)
    admins = UserPublicSerializer(many=True, read_only=True)
    created_by = UserPublicSerializer(read_only=True)

    class Meta:
        model = GroupThread
        fields = '__all__'
        
        