from rest_framework import serializers
from .models import Blog
from user.models import User

class BlogSerializer(serializers.ModelSerializer):
    uname = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'blogtext', 'U_ID', 'uname']
    def get_uname(self, obj):
        try:
            user = User.objects.get(U_ID=obj.U_ID_id)
            return user.uname
        except User.DoesNotExist:
            return "Anonymous"