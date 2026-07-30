from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Application, CountyNotice
from .FSM_transitions import get_allowed_next_states

User = get_user_model()

# =====================================================================
# Authentication & Identity Serializers
# =====================================================================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes JWT token claims to inject RBAC context (roles) directly 
    into the encrypted client token payload.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Inject custom claims for front-end routing gates
        token['role'] = getattr(user, 'role', 'CITIZEN')
        token['email'] = user.email
        token['county_code'] = getattr(user, 'county_code', None) or "GLOBAL"
        
        return token


class UserRegistrationSerializer(serializers.ModelSerializer):
    """ Handles secure account creation with automatic password hashing. """
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'phone_number', 'county_code']
        extra_kwargs = {
            'role': {'required': False} 
        }

    def validate(self, attrs):
        # Enforcement rule: Officer accounts MUST be locked to a valid county zone string
        if attrs.get('role') == 'OFFICER' and not attrs.get('county_code'):
            raise serializers.ValidationError(
                {"county_code": "County officers must be assigned an administrative county location identifier."}
            )
        return attrs

    def create(self, validated_data):
        # account creation utilizing standard user manager for password hashing safety
        return User.objects.create_user(**validated_data)


# =====================================================================
# Core Operational Application Serializers (Fixes Your ImportError)
# =====================================================================

class CountyNoticeSerializer(serializers.ModelSerializer):
    """
    Serializes scraped or indexed local municipal announcements, 
    bursary forms, and regional tenders.
    """
    class Meta:
        model = CountyNotice
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializes workflow lifecycles for public applications. Automatically 
    calculates dynamic variables like next available states for your UI buttons.
    """
    allowed_next_states = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'tracking_number', 'service_type', 'status', 
            'payload_data', 'county_code', 'created_at', 'updated_at',
            'user_email', 'allowed_next_states'
        ]
        read_only_fields = ['id', 'tracking_number', 'status', 'created_at', 'updated_at']

    def get_allowed_next_states(self, obj):
        """
        Invokes your state machine utility to inform the React frontend 
        exactly which transition states to render dynamically.
        """
        return get_allowed_next_states(obj.status)