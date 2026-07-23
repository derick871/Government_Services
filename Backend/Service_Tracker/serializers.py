from rest_framework import serializers
from .models import CountyNotice, Application, StatusLog
from .FSM_transitions import get_allowed_next_states

class CountyNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountyNotice
        fields = '__all__'


class StatusLogSerializer(serializers.ModelSerializer):
    changed_by_name = serializers.CharField(source='changed_by.get_full_name', read_only=True)

    class Meta:
        model = StatusLog
        fields = ['id', 'from_state', 'to_state', 'changed_by_name', 'comment', 'timestamp']