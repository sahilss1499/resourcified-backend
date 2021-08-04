from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework_jwt.settings import api_settings

from customauth.models import (User)
from posts.models import Institute, Branch

from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import auth
import jwt
from django.conf import settings
from rest_framework.response import Response
import random
from rest_framework import permissions




class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'role',
                  'full_name', 'branch', 'institute')
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            },
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=255, min_length=3, write_only=True)
    password = serializers.CharField(
        max_length=68, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)
    token = serializers.CharField(
        max_length=68, min_length=6, read_only=True)
    full_name = serializers.CharField(
        max_length=68, min_length=6, read_only=True)


    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'token',
                  'id','full_name','role', 'institute', 'branch']
        extra_kwargs = {
            'role':{'read_only':True},
            'institute':{'read_only':True},
            'branch':{'read_only':True},
            }

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        try:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        return {
            'email': user.email,
            'username': user.username,
            'full_name': user.full_name,
            'token': token,
            'id': user.id,
            'role': user.role,
            'branch': user.branch,
            'institute': user.institute,
        }
        return super().validate(data)


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ('__all__')

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('__all__')

class UserProfileSerializer(serializers.ModelSerializer):
    
    institute = InstituteSerializer()
    branch = BranchSerializer()
    class Meta:
        model = User
        fields = ('id','email','phone','full_name','role','branch','institute','profile_image','gender','degree')
        extra_kwargs = {
            'id':{'read_only':True},
            'email':{'read_only':True},
            'role':{'read_only':True},
            'institute':{'read_only':True},
            'branch':{'read_only':True},
            }