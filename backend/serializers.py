"""
##author：liangqian at 20230608
"""
from django import forms
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from  collections import OrderedDict
from .models import *

from rest_framework.fields import empty, CharField, DateField, TimeField, IntegerField, BooleanField, FileField, FloatField,  DateTimeField, ChoiceField

class PKOnlyObject:
 
    def __init__(self, pk):
        self.pk = pk
 
    def __str__(self):
        return "%s" % self.pk

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



 

# class SamplingSerializer(serializers.ModelSerializer):
    # usern = serializers.ReadOnlyField(source='usern.username')  # 外键字段 只读
    # #SID=serializers.SerializerMethodField()
    # class Meta:
        # model = Sampling  # 写法和上面的CourseForm类似
        # # exclude = ('id', )  # 注意元组中只有1个元素时不能写成("id")
        # # fields = ('id', 'name', 'introduction', 'teacher', 'price', 'created_at', 'updated_at')
        # fields = '__all__'
        # depth = 2

    # #def get_SID(self,obj):
    # #   current_project=obj
    # #   return current_project.sid


class SamplingSerializer(serializers.ModelSerializer):
    usern = serializers.ReadOnlyField(source='usern.username')  # 外键字段 只读
    #SID=serializers.SerializerMethodField()
    class Meta:
        model = Sampling  # 写法和上面的CourseForm类似
        # exclude = ('id', )  # 注意元组中只有1个元素时不能写成("id")
        # fields = ('id', 'name', 'introduction', 'teacher', 'price', 'created_at', 'updated_at')
        fields = '__all__'
        depth = 2



class StrainInfoSerializer(serializers.ModelSerializer):
    usern = serializers.ReadOnlyField(source='usern.username')  # 外键字段 只读
    sampleNo = serializers.ReadOnlyField(source="sampleNo.project")
    #SID=serializers.SerializerMethodField()
    class Meta:
        model = StrainInfo  # 写法和上面的CourseForm类似
        # exclude = ('id', )  # 注意元组中只有1个元素时不能写成("id")
        # fields = ('id', 'name', 'introduction', 'teacher', 'price', 'created_at', 'updated_at')
        fields = '__all__'
        depth = 2


class SequencingSerializer(serializers.ModelSerializer):
    usern = serializers.ReadOnlyField(source='usern.username')  # 外键字段 只读
    #SID=serializers.SerializerMethodField()
    class Meta:
        model = Sequencing  # 写法和上面的CourseForm类似
        # exclude = ('id', )  # 注意元组中只有1个元素时不能写成("id")
        # fields = ('id', 'name', 'introduction', 'teacher', 'price', 'created_at', 'updated_at')
        fields = '__all__'
        depth = 2


