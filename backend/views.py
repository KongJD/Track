# encoding: utf-8
import json
import os
import datetime
import random
import string

from celery.result import AsyncResult
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse,FileResponse,JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import APIView,AuthTokenSerializer
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import  *
from .RecreateLogEntry import *
import re
import logging

from userapp.models import NewUser
from .tasks import *
# 日志输出常量定义
logger = logging.getLogger('mylogger')

# Create your views here.


basedir="/public/Users/siteusr/website/Dmtrack2/media/result"
genedir=basedir+'/gene_predict'
speciesfind_dir=basedir+'/species_find'
Treedir=basedir+'/SNP_Tree'
anidir=basedir+'/ANI'
ARVFdir=basedir+'/ARVF'
Serotypedir=basedir+'/Serotype'
checkmdir=basedir+'/checkm'
AR_VFdir=basedir+'/AR-VF'
MSTdir=basedir+'/MST'
MLSTdir=basedir+'/MLST'
tmpdir=basedir+'/gBac'
onlinedir=basedir+'/pipline'
statusdir=basedir+'/task_log'
reads_snpdir= basedir+'/Reads_snp'

#采样表
class SamplingGeneric(GenericAPIView):
    queryset = Sampling.objects.all()
    serializer_class = SamplingSerializer

    def get(self, request, *args, **kwargs):
        """单查和群查"""
        if kwargs.get('pk'):
            cc = self.get_object()
            c_ser = self.get_serializer(cc)
            return Response(c_ser.data,status.HTTP_200_OK)
        # 查询所有数据
        c_list = self.get_queryset().filter(is_delete=False)  # 查询所有没有被删的记录

        # page = self.paginate_queryset(c_list)###使用paginate_queryset方法，进行分页操作；需要接收查询集参数；如果返回的数据为空，说明不进行分页操作，否则需要进行分页操作
        # if page is not None:
                # # 调用get_serializer，将page作为参数传给instance
            # serializer = self.get_serializer(instance=page, many=True)
            # # 分页必须调用get_paginated_response方法返回
            # return self.get_paginated_response(serializer.data)
        # else:
        c_list_ser = self.get_serializer(c_list, many=True)
        return Response(data=c_list_ser.data,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """单增和群增"""
        if isinstance(request.data, dict):
            c_ser = self.get_serializer(data=request.data)
            user_id=self.request.user.id
            #create_addition_log(user_id,c_ser)
            c_ser.is_valid(raise_exception=True)
            c_ser.save(usern=self.request.user)
            return Response(data=c_ser.data,status=status.HTTP_201_CREATED)
        elif isinstance(request.data, list):
            c_ser = self.get_serializer(data=request.data, many=True)
            c_ser.is_valid(raise_exception=True)
            c_ser.save(usern=self.request.user)
            return Response(data=c_ser.data,status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """单修和群修"""
        if kwargs.get('pk'):
            user_id=self.request.user.id
            c = self.get_object()
           #create_change_log(user_id,c,c,request.data)
            c_ser = self.get_serializer(instance=c, data=request.data, partial=True)
            c_ser.is_valid(raise_exception=True)
            c_ser.save(usern=self.request.user)
            return Response(data=c_ser.data,status=status.HTTP_201_CREATED)
        else:
            c_list = []
            modify_data = []
            for item in request.data:
                pk = item.pop('pk')
                c = self.get_queryset().get(pk=pk)
                #c = self.get_queryset().filter(pk=pk).first()  # 这样写也可以
                c_list.append(c)
                modify_data.append(item)
            c_ser = self.get_serializer(instance=c_list, data=modify_data, many=True, partial=True)
            c_ser.is_valid(raise_exception=True)
            c_ser.save(usern=self.request.user)
            return Response(c_ser.data,status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """单删和多删"""
        pk = kwargs.get('pk')
        pks = []
        if pk:
            pks.append(pk)
        else:
            pks = request.data.get('pks')
        ret = self.get_queryset().filter(pk__in=pks, is_delete=False).update(is_delete=True)
        if ret:
            return Response(data={'msg': '删除成功！删除了%s条数据' % ret})
        return Response(data={'msg': '没有可删除的数据...'})

##菌株信息管理表
class StrainInfoGeneric(GenericAPIView):
    queryset = StrainInfo.objects.all()
    serializer_class = StrainInfoSerializer

    def get(self, request, *args, **kwargs):
        """单查和群查"""
        if kwargs.get('pk'):
            cc = self.get_object()
            c_ser = self.get_serializer(cc)
            return Response(c_ser.data,status.HTTP_200_OK)
        # 查询所有数据
        c_list = self.get_queryset().filter(is_delete=False)  # 查询所有没有被删的记录

        # page = self.paginate_queryset(c_list)###使用paginate_queryset方法，进行分页操作；需要接收查询集参数；如果返回的数据为空，说明不进行分页操作，否则需要进行分页操作
        # if page is not None:
                # # 调用get_serializer，将page作为参数传给instance
            # serializer = self.get_serializer(instance=page, many=True)
            # # 分页必须调用get_paginated_response方法返回
            # return self.get_paginated_response(serializer.data)
        # else:
        c_list_ser = self.get_serializer(c_list, many=True)
        return Response(data=c_list_ser.data,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """单增和群增"""
        if isinstance(request.data, dict):
            c_ser = self.get_serializer(data=request.data)
            user_id=self.request.user.id
            #create_addition_log(user_id,c_ser)
            c_ser.is_valid(raise_exception=True)
            samplo = Sampling.objects.get(project=self.request.data.get('strainId'))
            c_ser.save(usern=self.request.user,sampleNo = samplo)
            return Response(data=c_ser.data,status=status.HTTP_201_CREATED)
        elif isinstance(request.data, list):
            c_ser = self.get_serializer(data=request.data, many=True)
            c_ser.is_valid(raise_exception=True)
            samplo = Sampling.objects.get(project="1")
            c_ser.save(usern=self.request.user,sampleNo = samplo)
            return Response(data=c_ser.data,status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """单修和群修"""
        if kwargs.get('pk'):
            user_id=self.request.user.id
            c = self.get_object()
           #create_change_log(user_id,c,c,request.data)
            c_ser = self.get_serializer(instance=c, data=request.data, partial=True)
            c_ser.is_valid(raise_exception=True)
            c_ser.save(usern=self.request.user)
            return Response(data=c_ser.data,status=status.HTTP_201_CREATED)
        else:
            c_list = []
            modify_data = []
            for item in request.data:
                pk = item.pop('pk')
                c = self.get_queryset().get(pk=pk)
                c_ser = self.get_serializer(instance=c, data=item, partial=True)
                c_ser.is_valid(raise_exception=True)
                c_ser.save(usern=self.request.user)
                #c = self.get_queryset().filter(pk=pk).first()  # 这样写也可以
                c_list.append(c)
                modify_data.append(item)

            # c_ser = self.get_serializer(instance=c_list, data=modify_data, many=True, partial=True)
            # c_ser.is_valid(raise_exception=True)
            # c_ser.save(usern=self.request.user)
            return Response(modify_data,status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """单删和多删"""
        pk = kwargs.get('pk')
        pks = []
        if pk:
            pks.append(pk)
        else:
            pks = request.data.get('pks')
        ret = self.get_queryset().filter(pk__in=pks, is_delete=False).update(is_delete=True)
        if ret:
            return Response(data={'msg': '删除成功！删除了%s条数据' % ret})
        return Response(data={'msg': '没有可删除的数据...'})

##测序实验信息管理表
class SequencingGeneric(GenericAPIView):
    queryset = Sequencing.objects.all()
    serializer_class = SequencingSerializer

    def get(self, request, *args, **kwargs):
        """单查和群查"""
        if kwargs.get('pk'):
            cc = self.get_object()
            c_ser = self.get_serializer(cc)
            return Response(c_ser.data,status.HTTP_200_OK)
        # 查询所有数据
        c_list = self.get_queryset().filter(is_delete=False)  # 查询所有没有被删的记录

        # page = self.paginate_queryset(c_list)###使用paginate_queryset方法，进行分页操作；需要接收查询集参数；如果返回的数据为空，说明不进行分页操作，否则需要进行分页操作
        # if page is not None:
                # # 调用get_serializer，将page作为参数传给instance
            # serializer = self.get_serializer(instance=page, many=True)
            # # 分页必须调用get_paginated_response方法返回
            # return self.get_paginated_response(serializer.data)
        # else:
        c_list_ser = self.get_serializer(c_list, many=True)
        return Response(data=c_list_ser.data,status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """单增和群增"""
        if isinstance(request.data, dict):
            c_ser = self.get_serializer(data=request.data)
            user_id=self.request.user.id
            #create_addition_log(user_id,c_ser)
            c_ser.is_valid(raise_exception=True)
            c_ser.save(usern=self.request.user)
            return Response(data=c_ser.data,status=status.HTTP_201_CREATED)
        elif isinstance(request.data, list):
            c_ser = self.get_serializer(data=request.data, many=True)
            c_ser.is_valid(raise_exception=True)
            c_ser.save(usern=self.request.user)
            return Response(data=c_ser.data,status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """单修和群修"""
        if kwargs.get('pk'):
            user_id=self.request.user.id
            c = self.get_object()
           #create_change_log(user_id,c,c,request.data)
            c_ser = self.get_serializer(instance=c, data=request.data, partial=True)
            c_ser.is_valid(raise_exception=True)
            c_ser.save(usern=self.request.user)
            return Response(data=c_ser.data,status=status.HTTP_201_CREATED)
        else:
            c_list = []
            modify_data = []
            for item in request.data:
                pk = item.pop('pk')
                c = self.get_queryset().get(pk=pk)
                #c = self.get_queryset().filter(pk=pk).first()  # 这样写也可以
                c_list.append(c)
                modify_data.append(item)
            c_ser = self.get_serializer(instance=c_list, data=modify_data, many=True, partial=True)
            c_ser.is_valid(raise_exception=True)
            c_ser.save(usern=self.request.user)
            return Response(c_ser.data,status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """单删和多删"""
        pk = kwargs.get('pk')
        pks = []
        if pk:
            pks.append(pk)
        else:
            pks = request.data.get('pks')
        ret = self.get_queryset().filter(pk__in=pks, is_delete=False).update(is_delete=True)
        if ret:
            return Response(data={'msg': '删除成功！删除了%s条数据' % ret})
        return Response(data={'msg': '没有可删除的数据...'})

# 批量上传fasta获取的接口

##工具
class Tools_SP(APIView):
    def post(self, request,*args,**kwargs):##
        jobid=tid_maker()
        a=request.FILES.getlist('genomefiles')
        #email=request.POST.get('email')
	#username = request.user
        path=os.path.join(settings.MEDIA_ROOT,"genome",str(datetime.datetime.now().year),str(datetime.datetime.now().month),jobid)
        isExists=os.path.exists(path)
        context={}
        if not isExists:
            os.makedirs(path)
        if len(a)>=1:
            name=''
            filelst=''
            for f in request.FILES.getlist('genomefiles'):
                print(path,f.name)
                destination=open(path +'/'+ f.name,'wb+')
                name+=f.name+";"
                filelst+=path+"/"+f.name+";"
                for chunk in f.chunks(chunk_size=1024*100):
                    destination.write(chunk)
                destination.close()
            username=NewUser.objects.get(username=self.request.user)
            d=Multi_Upload(usern=username,path=path,filename=name,tasktype='spFinder',jobID=jobid)
            d.save()
            timenow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            t=Tasklist(usern=username,jobid=jobid,protocol="物种鉴定",submit_date=timenow,tag="Spfinder")
            t.save()
            replace_reg=re.compile(r';$')
            filelst=replace_reg.sub('',filelst)
            outdir=speciesfind_dir+"/"+jobid
            tmpdir_t=tmpdir+"/"+jobid
            Job2Task.objects.create(usern=username,jobID=jobid,task_name="spFinder")
            celery_result=species_find.delay(filelst,outdir,tmpdir_t,jobid)
            res=AsyncResult(celery_result.task_id)
            celery_id=celery_result.id
            j1=JobStat(usern=username,jobID=jobid,celery_task_id=celery_id)
            j1.save()

            context['jobid'] =jobid
            context['taskinfo'] = str(celery_id)+'|'+str(jobid)+'|spFinder'
            return Response(context,status=status.HTTP_200_OK)
        else:
            return Response({'res':"error",'msg':'未上传的基因组序列文件！'},status=status.HTTP_400_BAD_REQUEST)

class Tools_GENE(APIView):
    def post(self, request,*args,**kwargs):
        jobid=tid_maker()
	#username = request.username
	#context = {}
        print(request.POST)
        a=request.FILES.getlist('genomefiles')
        path=os.path.join(settings.MEDIA_ROOT,"genome",str(datetime.datetime.now().year),str(datetime.datetime.now().month),jobid)
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        if len(a)>=1:
            name=''
            filelst=''
            for f in request.FILES.getlist('genomefiles'):
                print(path,f.name)
                destination=open(path +'/'+ f.name,'wb+')
                name+=f.name+";"
                filelst+=path+"/"+f.name+";"
                for chunk in f.chunks(chunk_size=1024*100):
                    destination.write(chunk)
                destination.close()
            username = NewUser.objects.get(username=self.request.user)
            context = {}
            d=Multi_Upload(usern=username,path=path,filename=name,tasktype='gene',jobID=jobid)
            d.save()
            timenow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            t=Tasklist(usern=username,jobid=jobid,protocol="基因预测",submit_date=timenow,tag="gene")
            t.save()
            replace_reg=re.compile(r';$')
            filelst=replace_reg.sub('',filelst)
            outdir=genedir+"/"+jobid
            tmpdir_t=tmpdir+"/"+jobid
            Job2Task.objects.create(usern=username,jobID=jobid,task_name="gene")
            celery_result=gene_predict.delay(filelst,outdir,tmpdir_t,jobid)
            celery_id=celery_result.id
            j1=JobStat(usern=username,jobID=jobid,celery_task_id=celery_id)
            j1.save()

            context['jobid'] =jobid
            context['taskinfo'] = str(celery_id)+'|'+str(jobid)+'|gene'
            return Response(context,status=status.HTTP_200_OK)
        else:
            return Response({'res':"error",'msg':'未上传的基因组序列文件！'},status=status.HTTP_400_BAD_REQUEST)

# class Tools_ANI(APIView):
    # def post(self, request,*args,**kwargs):
        # jobid=tid_maker()
        # a=request.FILES.getlist('genomefiles')
        # #email=request.POST.get('email')
        # path=os.path.join(settings.MEDIA_ROOT,"genome",str(datetime.datetime.now().year),str(datetime.datetime.now().month),jobid)
        # isExists=os.path.exists(path)
        # context={}
        # anilist=((1,'gANI'),(2,'orthoANI'))
        # #print(request.POST['Form_ani_method'])
        # method=anilist[int(request.POST['Form_ani_method'])-1][1]

        # if not isExists:
            # os.makedirs(path)
        # if len(a)>1:
            # name=''
            # filelst=''
            # for f in request.FILES.getlist('genomefiles'):
                # print(path,f.name)
                # destination=open(path +'/'+ f.name,'wb+')
                # name+=f.name+";"
                # filelst+=path+"/"+f.name+";"
                # for chunk in f.chunks(chunk_size=1024*100):
                    # destination.write(chunk)
                # destination.close()
            # d=Multi_Upload(user=username,path=path,filename=name,tasktype='ANI',jobID=jobid,marker=method,tag="ANI")
            # d.save()
            # replace_reg=re.compile(r';$')
            # filelst=replace_reg.sub('',filelst)
            # Job2Task.objects.create(user=username,jobID=jobid,task_name="ANI")
            # timenow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # t=Tasklist(user=username,jobid=jobid,protocol="计算ANI",submit_date=timenow)
            # t.save()
            # outdir=anidir+"/"+jobid
            # anitmpdir=tmpdir+"/"+jobid
            # print(method)
            # celery_result=ANIcalculator.delay(filelst,method,outdir,anitmpdir,jobid)
            # celery_id=celery_result.id
            # j1=JobStat(user=username,jobID=jobid,celery_task_id=celery_id)
            # j1.save()

            # context['jobid'] =jobid
            # context['taskinfo'] = str(celery_id)+'|'+str(jobid)+'|ANI'
            # return Response(context,status=status.HTTP_200_OK)
        # else:
            # return Response({'res':"error",'msg':'上传2个或2个以上的基因组序列文件！'},status=status.HTTP_400_BAD_REQUEST)

        
# class Tools_AR_VF(APIView):
    # def post(self, request,*args,**kwargs):
        # jobid=tid_maker()
        
        # a=request.FILES.getlist('genomefiles')
        # path=os.path.join(settings.MEDIA_ROOT,"genome",str(datetime.datetime.now().year),str(datetime.datetime.now().month),jobid)
        # isExists=os.path.exists(path)
        # typelist=((1,'genome'),(2,'gene'))
        # analylist=((1,'resistance gene'),(2,'virulent factor'),(3,'all'))
        # #print(request.POST['Form_ani_method'])
        # type1=typelist[int(request.POST['Form_file_type'])-1][1]
        # option=analylist[int(request.POST['Form_ARVF_type'])-1][1]
        
        # if not isExists:
            # os.makedirs(path)
        # if len(a)>=1:
            # name=''
            # filelst=''
            # for f in request.FILES.getlist('genomefiles'):
                # print(path,f.name)
                # destination=open(path +'/'+ f.name,'wb+')
                # name+=f.name+";"
                # filelst+=path+"/"+f.name+";"
                # for chunk in f.chunks(chunk_size=1024*100):
                    # destination.write(chunk)
                # destination.close()
            # d=Multi_Upload(user=username,path=path,filename=name,tasktype='ARVF',jobID=jobid,marker=option,tag="ARVF")
            # d.save()
            # replace_reg=re.compile(r';$')
            # filelst=replace_reg.sub('',filelst)
            # Job2Task.objects.create(user=username,jobID=jobid,task_name="ARVF")
            # timenow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # t=Tasklist(user=username,jobid=jobid,protocol="耐药毒力分析",submit_date=timenow)
            # t.save()
            # outdir=ARVFdir+"/"+jobid
            # ARVFtmpdir=tmpdir+"/"+jobid
            # celery_result=AR_VF_analysis.delay(filelst,type1,option,outdir,ARVFtmpdir,jobid)
            # celery_id=celery_result.id
            # j1=JobStat(user=username,jobID=jobid,celery_task_id=celery_id)
            # j1.save()

            # context['jobid'] =jobid
            # context['taskinfo'] = str(celery_id)+'|'+str(jobid)+'|ARVF'
            # return Response(context,status=status.HTTP_200_OK)
        # else:
            # return Response({'res':"error",'msg':'文件上传有误，请重新上传！'},status=status.HTTP_400_BAD_REQUEST)


# #
# class Tools_Serotype(APIView):
    # def post(self, request,*args,**kwargs):
        # jobid=tid_maker()
        # context['jobid']=jobid
        # file=request.FILES.get('genomefile')
        # path=os.path.join(settings.MEDIA_ROOT,"genome",str(datetime.datetime.now().year),str(datetime.datetime.now().month),jobid)
        # isExists=os.path.exists(path)
        # splist=((1,'Acinetobacter baumannii'),(2,'Escherichia coli'),(3,'Klebsiella pneumoniae'),(4,'Salmonella enterica'))

        # sp=splist[int(request.POST['specisen'])-1][1]
        # print(sp)
        # if not isExists:
            # os.makedirs(path)

        # destination=open(path +'/'+ file.name,'wb+')
        # for chunk in file.chunks(chunk_size=1024*100):
            # destination.write(chunk)
        # destination.close()
        # infile=path +'/'+ file.name
        # print(path +'/'+ file.name)
        # print("****test****")
        # d=Multi_Upload(user=username,path=path,filename=file.name,tasktype='Serotype',jobID=jobid,marker=sp,tag="Serotype")
        # d.save()
        # Job2Task.objects.create(user=username,jobID=jobid,task_name="Serotype")
        # print("222!!!!!!")
        # timenow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # t=Tasklist(user=username,jobid=jobid,protocol="血清型分型",submit_date=timenow)
        # t.save()
        # outdir=Serotypedir+"/"+jobid+"/"
        # celery_result=Serotype_analysis.delay(infile,sp,outdir,jobid)
        # celery_id=celery_result.id
        # j1=JobStat(user=username,jobID=jobid,celery_task_id=celery_id)
        # j1.save()

        # context['jobid'] =jobid
        # context['taskinfo'] = str(celery_id)+'|'+str(jobid)+'|Serotype'
        # return Response(context,status=status.HTTP_200_OK)
    # else:
        # return Response({'res':"error",'msg':'文件上传有误，请重新上传！'},status=status.HTTP_400_BAD_REQUEST)

# class Tools_ReadsSNP(APIView):
    # def post(self, request,*args,**kwargs):
        # jobid=tid_maker()
        # context['jobid']=jobid
        # #print(request.POST)
        # file=request.FILES.get('genomefile')
        # infqdir=request.POST.get('inputdir')
        # path=os.path.join(settings.MEDIA_ROOT,"genome",str(datetime.datetime.now().year),str(datetime.datetime.now().month),jobid)
        # isExists=os.path.exists(path)
        # bootlist=((1,'100'),(2,'1000'))

        # boot=bootlist[int(request.POST['bootstrap'])-1][1]

        # if not isExists:
            # os.makedirs(path)

        # destination=open(path +'/'+ file.name,'wb+')
        # for chunk in file.chunks(chunk_size=1024*100):
            # destination.write(chunk)
        # destination.close()
        # reffile=path +'/'+ file.name
        # print(path +'/'+ file.name)
        # d=Multi_Upload(user=username,path=path,filename=file.name,tasktype='ReadsSNP',jobID=jobid,marker=infqdir,tag="ReadsSNP")
        # d.save()
        # Job2Task.objects.create(user=username,jobID=jobid,task_name="ReadsSNP")
        # timenow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # t=Tasklist(user=username,jobid=jobid,protocol="Reads水平检测SNP",submit_date=timenow)
        # t.save()
        # outdir=reads_snpdir+"/"+jobid+"/"
        # celery_result=reads_snp_analysis.delay(infqdir,reffile,boot,outdir,jobid)
        # celery_id=celery_result.id
        # j1=JobStat(user=username,jobID=jobid,celery_task_id=celery_id)
        # j1.save()
        # context['jobid'] =jobid
        # context['taskinfo'] = str(celery_id)+'|'+str(jobid)+'|Serotype'
        # return Response(context,status=status.HTTP_200_OK)
    # else:
        # return Response({'res':"error",'msg':'文件上传有误，请重新上传！'},status=status.HTTP_400_BAD_REQUEST)


# class Tools_ReadsSNP(APIView):
    # def post(self, request,*args,**kwargs):
        # context={}
        # jobid=tid_maker()
        # a=request.FILES.getlist('genomefiles')

        # path=os.path.join(settings.MEDIA_ROOT,"genome",str(datetime.datetime.now().year),str(datetime.datetime.now().month),jobid)
        # isExists=os.path.exists(path)
        # if not isExists:
            # os.makedirs(path)
        # if len(a)>=1:
            # name=''
            # filelst=''
        # for f in request.FILES.getlist('genomefiles'):
            # print(path,f.name)
            # destination=open(path +'/'+ f.name,'wb+')
            # name+=f.name+";"
            # filelst+=path+"/"+f.name+";"
            # for chunk in f.chunks(chunk_size=1024*100):
                # destination.write(chunk)
            # destination.close()
        # d=Multi_Upload(user=username,path=path,filename=name,tasktype='checkm',jobID=jobid)
        # d.save()
        # timenow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # t=Tasklist(user=username,jobid=jobid,protocol="基因组质量评估",submit_date=timenow)
        # t.save()
        # replace_reg=re.compile(r';$')
        # filelst=replace_reg.sub('',filelst)
        # outdir=checkmdir+"/"+jobid
        # Job2Task.objects.create(user=username,jobID=jobid,task_name="checkm")
        # celery_result=checkm.delay(filelst,outdir,jobid)
        # celery_id=celery_result.id
        # j1=JobStat(user=username,jobID=jobid,celery_task_id=celery_id)
        # j1.save()
        # context['jobid'] =jobid
        # context['taskinfo'] = str(celery_id)+'|'+str(jobid)+'|checkm'
        # return Response(context,status=status.HTTP_200_OK)
    # else:
        # return Response({'res':"error",'msg':'文件上传有误，请重新上传！'},status=status.HTTP_400_BAD_REQUEST)



def tid_maker():
        return '{0:%Y%m%d%H%f}'.format(datetime.datetime.now())+''.join(random.sample(string.ascii_letters + string.digits, 4))
