from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes JWT token claims to inject RBAC context (roles) directly 
    into the encrypted client token payload.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Inject custom claims for front-end routing gates
        token['role'] = user.role
        token['email'] = user.email
        token['county_code'] = user.county_code or "GLOBAL"
        
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
        #  account creation to custom manager for password hashing safety
        return User.objects.create_user(**validated_data)