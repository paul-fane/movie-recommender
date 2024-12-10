from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    re_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 're_password')
    
    def validate(self, data):
        """
        Check if password and re_password match.
        """
        if data['password'] != data['re_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Create a new user with a hashed password.
        """
        validated_data.pop('re_password')  # Remove re_password as it's not needed for user creation
        user = User.objects.create_user(**validated_data)
        return user
