from django import forms
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        re_data = {'data': data, 'code': 200, 'message': 'success', 'user_id': self.user.id}
        return re_data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'
