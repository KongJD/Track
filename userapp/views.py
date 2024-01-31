from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import APIView,AuthTokenSerializer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from userapp.models import  NewUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from .serializers import  MyTokenObtainPairSerializer
from .permissions import IsOwnerOrReadOnly
from .models import *
from .getIP import *
import datetime
# Create your views here.
import logging
# 日志输出常量定义
logger = logging.getLogger('mylogger')

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        ip=getIP(request)
        try:
            serializer.is_valid(raise_exception=True)
            time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print("abcy")
            #print(self.request.data['username'])
            usern=self.request.data['username']
            logger.info("user:%s 于 [%s] 登录成功,ip地址为%s at"%(usern,str(time1),str(ip)))
            #ip2 = request.META.get('REMOTE_ADDR')
            actions="%s 于 %s 登录"%(usern,ip)
            #AuditEntry.objects.create(action=actions, ip=ip, username=usern)
            #logger.info("%s login %s"%(self.request.user,ip))
        except TokenError as e:
            time1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            usern=self.request.data['username']
            logger.info("user:%s 于 [%s] 登录失败,ip地址为%s at"%(usern,str(time1),str(ip)))
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
