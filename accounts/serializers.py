from typing import Union
from django.db.models import fields
from rest_framework import serializers
from accounts.models import User, UserAddress
from accounts.types import NewUser, NewUserSerializer, UserLogin
from accounts.usecases import create_user_account

class UserAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        exclude = ('user',)

class UserSerializer(serializers.ModelSerializer):
    address = UserAddressSerializers(many=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'
        
    def create(self, validated_data:NewUserSerializer):
        validated_data.pop("confirm_password")
        return create_user_account(validated_data)

    def validate(self, validated_data:NewUserSerializer)->NewUserSerializer:
        if not validated_data['password'] or not validated_data['confirm_password']:
            raise serializers.ValidationError('Enter a password and confirm it')
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError('Password don\'t match')
        return validated_data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
            
        
