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

class ApplicationDetailSerializer(serializers.ModelSerializer):
    logs = StatusLogSerializer(many=True, read_only=True)
    citizen_name = serializers.CharField(source='citizen.get_full_name', read_only=True)
    allowed_actions = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id', 'tracking_number', 'citizen_name', 'county_id', 
            'service_type', 'status', 'payload_data', 
            'created_at', 'updated_at', 'allowed_actions', 'logs'
        ]

    def get_allowed_actions(self, obj):
        """Tells the frontend UI which action buttons to show based on the FSM context."""
        return get_allowed_next_states(obj.status)


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['county_id', 'service_type', 'payload_data']

    def create(self, validated_data):
        import uuid
        # Automatically generate a clean structural tracking layout prefix
        validated_data['tracking_number'] = f"TRK-{uuid.uuid4().hex[:8].upper()}"
        return super().create(validated_data)