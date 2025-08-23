from rest_framework import serializers
from .models import SystemInfo, Process

class SystemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = "__all__"

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"


