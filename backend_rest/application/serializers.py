from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'APP_ID', 'id', 'jobrole', 'company', 'link',
            'status', 'platform', 'location', 'notes', 'changed_at'
        ]
        read_only_fields = ['APP_ID', 'changed_at']