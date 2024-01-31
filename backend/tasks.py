# -*- coding: utf-8 -*-  
# Create your tasks here
#author:liangqian,norah-liang@dmicrobe.com at 20200108
from __future__ import absolute_import, unicode_literals

from eventlet.green.thread import get_ident

from celery import shared_task
from django.core.mail import send_mail,EmailMultiAlternatives
#from Bacapp.send_email import send_email
import io
import subprocess
import sys, getopt
import os
import datetime
import time
import re
import django
from django.db import connection

#sys.path.append("/public/Users/liangq/website/bacsite");
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bacsite.settings")
#django.setup()

python3="/public/Biosoft/Python-3.8.6/local/bin/python3"
stautsdir="/public/Users/siteusr/website/Dmtrack2/media/result/task_log"
bind="/public/Users/liangq/pipeline/bac_bin"
fastq_statPE="/public/Biosoft/fastq_stat/fastq_statPE"
fastq_statSE="/public/Biosoft/fastq_stat/fastq_statSE"
pauvre="/public/Biosoft/Python-3.8.6/local/bin/pauvre"
num=0

#from Bacapp.models import  identifyTemp,identifyTRe,ResultInfo,Samples

@shared_task
def deal_result(outdir,fq1,fq2):
    tagfile=outdir+"/sp/Taxonomy.txt"
    genomesp=''
    if os.path.exists(tagfile):
        with open (tagfile,'r') as handle:
            linest=handle.readlines()
            lines=linest[0].strip("\n")
            cut=lines.split("\t")
            genomesp=cut[0]
    print(genomesp)
    datanum=''
    datafile=outdir+"/data.stat.txt"
    if os.path.exists(datafile):
        with open(datafile,'r') as handle:
            linest=handle.readlines()
            lines1=linest[1].strip("\n")
            cut=lines1.split("\t")
            datanum=cut[1].replace(',','')
            datanum=round(int(datanum)/1000000,2)
    else:
        os.system("{fastq_statPE} {fq1} {fq2} >{outdir}/stat.txt".format(fastq_statPE=fastq_statPE,fq1=fq1,fq2=fq2,outdir=outdir))
        with open(outdir+"/stat.txt",'r') as handle:
            linest=handle.readlines()
            lines2=linest[1].strip("\n")
            cut=lines2.split("\t")
            datanum=cut[1].replace(',','')
            datanum=round(int(datanum)/1000000,2)
    print(datanum)
    checkmfile=outdir+"/genome.eva.txt"
    checkm=''
    if os.path.exists(checkmfile):
        with open(checkmfile,'r') as handle:
            linest=handle.readlines()
            lines=linest[1].strip("\n")
            cut=lines.split("\t")
            checkm="Completeness:"+str(cut[0])+"; Contamination:"+str(cut[1])  
    print(checkm)
    if len(str(datanum))>0:
        datanum=str(datanum)+"Mb"
    print(datanum)
    return genomesp,datanum,checkm
        
@shared_task
def deal_result2(outdir,fq1):
    tagfile=outdir+"/sp/Taxonomy.txt"
    genomesp=''
    if os.path.exists(tagfile):
        with open (tagfile,'r') as handle:
            linest=handle.readlines()
            lines=linest[0].strip("\n")
            cut=lines.split("\t")
            genomesp=cut[0]
    datanum=''
    datafile=outdir+"/data.stat.txt"
    if os.path.exists(datafile):
        with open(datafile,'r') as handle:
            linest=handle.readlines()
            lines1=linest[1].strip("\n")
            cut=lines1.split("\t")
            datanum=cut[1].replace(',','')
            datanum=round(int(datanum)/1000000,2)
    
    else:
        os.system("{fastq_statSE} {fq1} >{outdir}/stat.txt".format(fastq_statSE=fastq_statSE,fq1=fq1,outdir=outdir))
        with open(outdir+"/stat.txt",'r') as handle:
            linest=handle.readlines()
            lines2=linest[1].strip("\n")
            cut=lines2.split("\t")
            datanum=cut[1].replace(',','')
            datanum=round(int(datanum)/1000000,2)
    checkmfile=outdir+"/genome.eva.txt"
    checkm=''
    if os.path.exists(checkmfile):
        with open(checkmfile,'r') as handle:
            linest=handle.readlines()
            lines=linest[1].strip("\n")
            cut=lines.split("\t")
            checkm="Completeness:"+str(cut[0])+"; Contamination:"+str(cut[1])            
    if len(str(datanum))>0:
        datanum=str(datanum)+"Mb"
    #print(genomesp)
    #print(datanum)
    #print(checkm)
    return genomesp,datanum,checkm
    
@shared_task
def deal_result3(outdir,fq):
    tagfile=outdir+"/sp/Taxonomy.txt"
    genomesp=''
    if os.path.exists(tagfile):
        with open (tagfile,'r') as handle:
            linest=handle.readlines()
            lines=linest[0].strip("\n")
            cut=lines.split("\t")
            genomesp=cut[0]
    datanum=''
    datafile=outdir+"/data.stat.txt"
    if os.path.exists(datafile):
        with open(datafile,'r') as handle:
            linest=handle.readlines()
            lines1=linest[1].strip("\n")
            cut=lines1.split("\t")
            datanum=cut[1].replace(',','')
            datanum=round(int(datanum)/1000000,2)
    else:
        os.system("{pauvre} stats -f {fq} >{outdir}/stat.txt".format(pauvre=pauvre,fq=fq,outdir=outdir))
        with open(outdir+"/stat.txt",'r') as handle:
            linest=handle.readlines()
            lines2=linest[3].strip("\n")
            #print(lines2)
            datag=re.search(r'numBasepairs: (?P<data>\d+)$',lines2)
            #print(datag)
            #print(datag.group('data'))
            if datag !=None:
                datanum=format(int(datag.group(1))/1000000,'.2f')
    print(datanum)
    checkmfile=outdir+"/genome.eva.txt"
    checkm=''
    if os.path.exists(checkmfile):
        with open(checkmfile,'r') as handle:
            linest=handle.readlines()
            lines=linest[1].strip("\n")
            cut=lines.split("\t")
            checkm="Completeness:"+str(cut[0])+"; Contamination:"+str(cut[1])
    print(checkm)
    if len(str(datanum))>0:
        datanum=str(datanum)+"Mb"
    print(genomesp)
    return genomesp,datanum,checkm
       
@shared_task
def pipPE(fq1,fq2,outdir,Tmpdir,jobid,readlen,Trimmomatic,cut,qc,kmer,default,sample):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))  
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    try:   
        cmd=''
        if default=="yes":
            cmd="python3 {bind}/3.pipline/run.piplinePE.py -1 {fq1} -2 {fq2}  -o {outdir} -t {tmp} -c {cut} -q {qc} -n {sample}".format(bind=bind,fq1=fq1,fq2=fq2,outdir=outdir,tmp=Tmpdir,cut=cut,qc=qc,sample=sample)
        else:
            cmd="python3 {bind}/3.pipline/run.piplinePE.py -1 {fq1} -2 {fq2}  -o {outdir} -t {tmp} -c {cut} -q {qc}  -l {readlen} -i {trimm}  -k {kmer} -n {sample}".format(bind=bind,fq1=fq1,fq2=fq2,outdir=outdir,tmp=Tmpdir,cut=cut,qc=qc,readlen=readlen,trimm=Trimmomatic,kmer=kmer,sample=sample)
        os.system(cmd)
        print(cmd)
        subject='Report of Online pipeline from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/pipe/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact us   http://fbac.dmicrobe.cn/index ,this is an automated email, please do not reply.\n\nKind regards\nfBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&ensp;&ensp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact us <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>, this is an automated email, please do not reply.</p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        tagfile=outdir+"/sp/Taxonomy.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        #time.sleep(10)
        #send_email(email,subject,message,html_content)
    except:
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))       
    return outdir,jobid
    
@shared_task
def pipPE2(fq1,fq2,outdir,Tmpdir,jobid,name,sample):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))  
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    try:
        cmd="python3 {bind}/3.pipline/run.piplinePE.py -1 {fq1} -2 {fq2}  -o {outdir} -t {tmp} -c yes -q yes -n {sample}".format(bind=bind,fq1=fq1,fq2=fq2,outdir=outdir,tmp=Tmpdir,sample=sample)
        os.system(cmd)
        subject='Report of Online pipeline from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/pipe/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact us   http://fbac.dmicrobe.cn/index ,this is an automated email, please do not reply.\n\nKind regards\nfBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&ensp;&ensp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact us <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>, this is an automated email, please do not reply.</p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        tagfile=outdir+"/sp/Taxonomy.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
            genomesp,datanum,checkm=deal_result(outdir,fq1,fq2)
            query=identifyTemp.objects.filter(jobID=jobid)
            if query:
                d=identifyTRe(user=name,strain=query[0].strain,library=query[0].library,Seq_platform=query[0].Seq_platform,datanum=datanum,result=genomesp,genome_checkm=checkm)
                print(query[0].strain)
                d.save()
                kk=Samples.objects.filter(user=name,strain=query[0].strain).first()
                print(kk)
                global num
                num=num+1
                assid="ass"+str(num).zfill(6)
                print(assid)
                if kk is None:
                    rr=ResultInfo(user=name,strain=query[0].strain,spname=genomesp,assID=assid,source='',isolation_time='')
                else:
                    rr=ResultInfo(user=name,strain=query[0].strain,spname=genomesp,assID=assid,source=kk.source,isolation_time=kk.isolation_time)
                print("test--ResultInfo")
                rr.save()
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        
        #time.sleep(10)
        #send_email(email,subject,message,html_content)
    except:
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))       
    return outdir,jobid
    
@shared_task
def pipSE(fq1,outdir,Tmpdir,jobid,readlen,Trimmomatic,cut,qc,kmer,default,sample):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))  
    if not os.path.exists(outdir):
         os.makedirs(outdir)
    try:
        cmd=''
        if default=="yes":
            cmd="python3 {bind}/3.pipline/run.piplineSE.py -1 {fq1}  -o {outdir} -t {tmp} -c {cut} -q {qc} -n {sample}".format(bind=bind,fq1=fq1,outdir=outdir,tmp=Tmpdir,cut=cut,qc=qc,sample=sample)
        else:
            cmd="python3 {bind}/3.pipline/run.piplineSE.py -1 {fq1}   -o {outdir} -t {tmp} -c {cut} -q {qc} -l {readlen} -i {trimm} -k {kmer} -n {sample}".format(bind=bind,fq1=fq1,outdir=outdir,tmp=Tmpdir,cut=cut,qc=qc,readlen=readlen,trimm=Trimmomatic,kmer=kmer,sample=sample)
        os.system(cmd)
        subject='Report of Online pipeline from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/pipe/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact us http://fbac.dmicrobe.cn/index ,this is an automated email, please do not reply.\n\nKind regards\nfBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&ensp;&ensp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact us <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>, this is an automated email, please do not reply.</p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        tagfile=outdir+"/sp/Taxonomy.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        #time.sleep(10)
        #send_email(email,subject,message,html_content)
    except:
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))       
    return outdir,jobid

@shared_task
def pipSE2(fq1,outdir,Tmpdir,jobid,name,sample):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))  
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    try:
        cmd="python3 {bind}/3.pipline/run.piplineSE.py -1 {fq1}  -o {outdir} -t {tmp} -c yes -q yes -n {sample} ".format(bind=bind,fq1=fq1,outdir=outdir,tmp=Tmpdir,sample=sample)
        os.system(cmd)
        subject='Report of Online pipeline from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/pipe/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact us http://fbac.dmicrobe.cn/index ,this is an automated email, please do not reply.\n\nKind regards\nfBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&ensp;&ensp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact us <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>, this is an automated email, please do not reply.</p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        tagfile=outdir+"/sp/Taxonomy.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
            genomesp,datanum,checkm=deal_result2(outdir,fq1)
            print(genomesp)
            print(datanum)
            print(checkm)
            query=identifyTemp.objects.filter(jobID=jobid)
            print(query) 
            if query:
                print("***test***")
                d=identifyTRe(user=name,strain=query[0].strain,library=query[0].library,Seq_platform=query[0].Seq_platform,datanum=datanum,result=genomesp,genome_checkm=checkm)
                print(query[0].strain)
                d.save()
                kk=Samples.objects.filter(user=name,strain=query[0].strain).first()
                print(kk)
                global num
                num=num+1
                assid="ass"+str(num).zfill(6)
                print(assid)
                if kk is None:
                    rr=ResultInfo(user=name,strain=query[0].strain,spname=genomesp,assID=assid,source='',isolation_time='')
                else:
                    rr=ResultInfo(user=name,strain=query[0].strain,spname=genomesp,assID=assid,source=kk.source,isolation_time=kk.isolation_time)
                print("test--ResultInfo")
                rr.save()
        else:
            line='fail+['+time1+']'
            
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        
        #time.sleep(10)
        #send_email(email,subject,message,html_content)
    except:
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))       
    return outdir,jobid


    
@shared_task
def pipSan(fq,outdir,Tmpdir,jobid,sequence_type,cut,qc,sample):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))  
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    try:
        cmd="python3 {bind}/3.pipline/run.piplineNano_Pb.py -f {fq}  -o {outdir} -t {tmp} -c {cut} -q {qc}  -s {sequence_type} -n {sample}".format(bind=bind,fq=fq,outdir=outdir,tmp=Tmpdir,cut=cut,qc=qc,checkm=checkm,sequence_type=sequence_type,sample=sample)
     
        os.system(cmd)
        subject='Report of Online pipeline from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/pipe/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact us http://fbac.dmicrobe.cn/index ,this is an automated email, please do not reply.\n\nKind regards\nfBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&ensp;&ensp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact us <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>, this is an automated email, please do not reply.</p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'

        tagfile=outdir+"/sp/Taxonomy.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        #time.sleep(10)
        #send_email(email,subject,message,html_content)
    except:
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))     
    return outdir,jobid

@shared_task
def pipSan2(fq,outdir,Tmpdir,jobid,sequence_type,name,sample):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))  
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    try:
        cmd="python3 {bind}/3.pipline/run.piplineNano_Pb.py -f {fq}  -o {outdir} -t {tmp} -c yes -q yes  -s {sequence_type} -n {sample}".format(bind=bind,fq=fq,outdir=outdir,tmp=Tmpdir,sequence_type=sequence_type,sample=sample)
        os.system(cmd)
        subject='Report of Online pipeline from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/pipe/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact us http://fbac.dmicrobe.cn/index ,this is an automated email, please do not reply.\n\nKind regards\nfBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&ensp;&ensp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact us <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>, this is an automated email, please do not reply.</p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        tagfile=outdir+"/sp/Taxonomy.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
            genomesp,datanum,checkm=deal_result3(outdir,fq)
            query=identifyTemp.objects.filter(jobID=jobid)
            if query:
                d=identifyTRe(user=name,strain=query[0].strain,library=query[0].library,Seq_platform=query[0].Seq_platform,datanum=datanum,result=genomesp,genome_checkm=checkm)
                print(query[0].strain)
                d.save()
                kk=Samples.objects.filter(user=name,strain=query[0].strain).first()
                print(kk)
                global num
                num=num+1
                assid="ass"+str(num).zfill(6)
                print(assid)
                if kk is None:
                    rr=ResultInfo(user=name,strain=query[0].strain,spname=genomesp,assID=assid,source='',isolation_time='')
                else:
                    rr=ResultInfo(user=name,strain=query[0].strain,spname=genomesp,assID=assid,source=kk.source,isolation_time=kk.isolation_time)
                print("test--ResultInfo")
                rr.save()
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        
        #time.sleep(10)
        #send_email(email,subject,message,html_content)
    except:
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))     
    return outdir,jobid
        
@shared_task
def pipCom(longfq,shortfq,outdir,Tmpdir,jobid,pair,sample):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file)) 
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    try:
        cmd="python3 {bind}/3.pipline/run.piplineCom.py -l {long} -s \"{short}\" -p {pair}  -o {outdir} -t {tmp} -e yes -n {sample}".format(bind=bind,long=longfq,short=shortfq,pair=pair,outdir=outdir,tmp=Tmpdir,sample=sample)
        os.system(cmd)
        subject='Report of Online pipeline from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/pipe/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact us http://fbac.dmicrobe.cn/index ,this is an automated email, please do not reply.\n\nKind regards\nfBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&ensp;&ensp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact us <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>, this is an automated email, please do not reply.</p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        tagfile=outdir+"/sp/Taxonomy.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        #time.sleep(10)
        #send_email(email,subject,message,html_content)
    except:
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))       
    return outdir,jobid

@shared_task
def pipCom2(longfq,shortfq,outdir,Tmpdir,jobid,pair,name,sample):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file)) 
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    try:
        cmd="python3 {bind}/3.pipline/run.piplineCom.py -l {long} -s \"{short}\" -p \"{pair}\"  -o {outdir} -t {tmp} -e yes -n {sample}".format(bind=bind,long=longfq,short=shortfq,pair=pair,outdir=outdir,tmp=Tmpdir,sample=sample)
        print(cmd)
        os.system(cmd)
        subject='Report of Online pipeline from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/pipe/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact us http://fbac.dmicrobe.cn/index ,this is an automated email, please do not reply.\n\nKind regards\nfBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&ensp;&ensp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/pipe/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact us <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>, this is an automated email, please do not reply.</p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
 
        tagfile=outdir+"/sp/Taxonomy.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
            genomesp,datanum,checkm=deal_result3(outdir,longfq)
            query=identifyTemp.objects.filter(jobID=jobid)
            if query:
                d=identifyTRe(user=name,strain=query[0].strain,library=query[0].library,Seq_platform=query[0].Seq_platform,datanum=datanum,result=genomesp,genome_checkm=checkm)
                print(query[0].strain)
                d.save()
                kk=Samples.objects.filter(user=name,strain=query[0].strain).first()
                print(kk)
                global num
                num=num+1
                assid="ass"+str(num).zfill(6)
                print(assid)
                if kk is None:
                    rr=ResultInfo(user=name,strain=query[0].strain,spname=genomesp,assID=assid,source='',isolation_time='')
                else:
                    rr=ResultInfo(user=name,strain=query[0].strain,spname=genomesp,assID=assid,source=kk.source,isolation_time=kk.isolation_time)
                print("test--ResultInfo")
                rr.save()
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))

        
        
    except:
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))       
    return outdir,jobid
        


@shared_task
def MLST_analysis(infile,sp_name,allefile,result):
    isExists=os.path.exists(result)
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))
    if not isExists:
        os.makedirs(result)
    exe=bind+"/5.MLST/run_MLST.pipeline.pl"
    com=subprocess.run(['perl',exe,'-s',sp_name,'-t',allefile,'-q',infile,'-o',result],stdout=subprocess.PIPE)
    out=com.stdout
    out=out.decode()
    cut=out.split('\n')
    res=cut[-1]
    print (res)
    error="task任务未运行成功，请检查文件格式以及物种名称并重新提交！"
    if com.returncode == 0:
        print("SUCCESS!")
        st=result+'/MLST.STtype.txt'
        if not os.path.exists(st):
            return error
            time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            line='success+['+time1+']'
            os.system("echo {line}>>{file}".format(line=line,file=status_file))          
        else:
            time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            line='success+['+time1+']'
            os.system("echo {line}>>{file}".format(line=line,file=status_file))
            return res
    else:
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        return error
    

@shared_task
def SNP_Tree(filelst,result,Tmpfiles,jobid):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))
    try:
        cmd="python3 {bind}/9.snp_tree/run.SNP_Tree.py -i \"{filelst}\" -o {result}".format(bind=bind,filelst=filelst,result=result)
        print(filelst)
        print(cmd)
        os.system(cmd)
        subject='Report of Phylogenetic from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed, please check the attached file for phylogenetic results. If you have any questions , contact us http://fbac.dmicrobe.cn/index,this is an automated email, please do not reply. \n\n Kind regards\nfBacGID at '+str(datetime.date.today()) +'\n'
        #recipient_list=[email]
        #from_email='norah-liang@dmicrobe.com'
        tagfile=result+"/snpTree.treefile.tre"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
 
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        time.sleep(10)
        #send_email(subject,message,[],recipient_list)
    except:
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(jobid +" error in SNP_analysis")
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
    return result,jobid


@shared_task
def Serotype_analysis(infile,sp,result,jobid):
    status_file=stautsdir+"/"+jobid+".log.txt"
    #w=open(status_file,'w')
    #w.write('start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"\n")
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))
    try:
        cmd="python3 {bind}/7.Serotype/run.Serotype.py -i \"{infile}\" -s \"{sp}\" -o {result}".format(bind=bind,infile=infile,sp=sp,result=result)
        os.system(cmd)
        print(cmd)
        subject='Report of Serotype from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/ARVF/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact http://fbac.dmicrobe.cn/index,this is an automated email, please do not reply. \n\nKind regards\n fBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&nbsp;&nbsp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/ARVF/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/ARVF/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>,this is an automated email, please do not reply. </p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        tagfile=result+"/sp.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        time.sleep(10)
        #send_email(email,subject,message,html_content)
    except:
        print(jobid+ " error in Serotype analysis")
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        #w.write('fail+['+time1+']'+"\n") 
    return result,jobid

@shared_task
def AR_VF_analysis(infile,type1,type2,result,Tmpfiles,jobid):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))
    try:
        cmd="python3 {bind}/6.ARDB_7.VFDB/run.ARVF.pipe.py -i \"{infile}\" -f {type1} -t \"{type2}\" -o {result}".format(bind=bind,infile=infile,type1=type1,type2=type2,result=result)
        os.system(cmd)
        print(cmd)
        subject='Report of AR/VF gene from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/ARVF/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact http://fbac.dmicrobe.cn/index,this is an automated email, please do not reply. \n\nKind regards\n fBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&nbsp;&nbsp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/ARVF/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/ARVF/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>,this is an automated email, please do not reply. </p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        tagfile=result+"/out.lst"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        time.sleep(10)
        #send_email(email,subject,message,html_content)
    except:
        print(jobid+ " error in AR_VF_analysis"+"\n")
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
    return result,jobid


@shared_task
def ANIcalculator(filelst,anitype,result,Tmpfiles,jobid):
    status_file=stautsdir+"/"+jobid+".log.txt" 
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))  
    try:
        if not os.path.exists(result):
            os.system("mkdir -m 755 -p {}".format(result))
        cmd="python3 {bind}/5.ANI/runANI.py {anitype} \"{filelst}\" {out}/{anitype} {temp}".format(bind=bind,anitype=anitype,filelst=filelst,out=result,temp=Tmpfiles)
        os.system(cmd)
        print(cmd)
        subject='Report of ANI calculator from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/ANI/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact http://fbac.dmicrobe.cn/index,this is an automated email, please do not reply. \n\nKind regards\n fBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&nbsp;&nbsp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/ANI/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/ANI/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>,this is an automated email, please do not reply. </p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        tagfile=result+"/"+anitype+"/all.ani.dist"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        time.sleep(10)
        #print("发送邮件")
        #send_email(email,subject,message,html_content)

    except:
        print(jobid + " error in ANIcalculator!")
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
    return result,jobid
    
@shared_task
def species_find(infile,result,Tmpfiles,jobid):
    conn = connection
    conn._thread_ident = get_ident()
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file)) 
    try:
        cmd="python3 {bind}/1.species/run.SpeciesFinder.py -i \"{infile}\" -o {result} ".format(bind=bind,infile=infile,result=result)
        os.system(cmd)
        subject='Report of Species Find from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/speciesfind/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact http://fbac.dmicrobe.cn/index,this is an automated email, please do not reply. \n\nKind regards\n fBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&nbsp;&nbsp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/speciesfind/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/speciesfind/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>,this is an automated email, please do not reply. </p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        print("SUCCESS!")
        tagfile=result+"/Identification_result.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        time.sleep(10)
        print("check")
        #conn.close_all()
        #send_email(email,subject,message,html_content)
    except:
        print(jobid + " error in species_find")
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file)) 
    return result,jobid


@shared_task
def gene_predict(infile,result,temp,jobid):
    conn = connection
    conn._thread_ident = get_ident()
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file))  
    try:
        cmd="python3 {bind}/2.gene/run.gene_predict.py -i \"{infile}\" -o {result} -d {temp} ".format(bind=bind,infile=infile,result=result,temp=temp)
        print(cmd)
        os.system(cmd)  
        subject='Report of Gene Prediction from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/genefind/task_result&jobid='+jobid+'\nIf you have any questions , please contact http://fbac.dmicrobe.cn/index,this is an automated email, please do not reply. \n\nKind regards\n fBacGID at '+ str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&nbsp;&nbsp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/genefind/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/genefind/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>,this is an automated email, please do not reply. </p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        time.sleep(10)
        #send_email(email,subject,message,html_content)
        tagfile=result+"/summary.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile)  and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
        #conn.close_all()
    except:
        print("发生异常")
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))  
    return result 
    
@shared_task
def checkm(infile,result,jobid):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file)) 
    try:
        cmd="python3 {bind}/4.Genome_evaluate/run.checkm.py -i \"{infile}\" -o {result} ".format(bind=bind,infile=infile,result=result)
        os.system(cmd)  
        subject='Report of Gene Prediction from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/genefind/task_result&jobid='+jobid+'\nIf you have any questions , please contact http://fbac.dmicrobe.cn/index,this is an automated email, please do not reply. \n\nKind regards\n fBacGID at '+ str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&nbsp;&nbsp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/genefind/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/genefind/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>,this is an automated email, please do not reply. </p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        time.sleep(10)
        #send_email(email,subject,message,html_content)
        tagfile=result+"/Genome_evaluate.txt"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile)  and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file)) 
    except:
        print("发生异常")
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
    return result 


@shared_task
def AR_VF_analysis(infile,type1,type2,result,Tmpfiles,jobid):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file)) 
    try:
        cmd="python3 {bind}/6.ARDB_7.VFDB/run.ARVF.pipe.py -i \"{infile}\" -f {type1} -t \"{type2}\" -o {result}".format(infile=infile,type1=type1,type2=type2,result=result)
        os.system(cmd)
        subject='Report of AR/VF gene from fBacGID'
        message='Dear Sir/Madam:\n  The task you submitted has been completed. Please visit the link http://fbac.dmicrobe.cn/tools/report/ARVF/task_result'+r'&jobid='+jobid+'\nIf you have any questions , please contact http://fbac.dmicrobe.cn/index,this is an automated email, please do not reply. \n\nKind regards\n fBacGID at '+str(datetime.date.today()) +'\n'
        html_content='<p>Dear Sir/Madam:</p> <p>&nbsp;&nbsp;The task you submitted has been completed. Please visit the link <a href=\"http://fbac.dmicrobe.cn/tools/report/ARVF/task_result&jobid='+jobid+'\">http://fbac.dmicrobe.cn/tools/report/ARVF/task_result&jobid='+jobid+'</a></p><p>If you have any questions , please contact <a href=\"http://fbac.dmicrobe.cn/index\">http://fbac.dmicrobe.cn/index</a>,this is an automated email, please do not reply. </p><p>Kind regards</p><p>fBacGID at '+str(datetime.date.today())+'</p>'
        time.sleep(10)
        #send_email(email,subject,message,html_content)
        tagfile=result+"/out.lst"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file)) 
    except:
        print("发生异常")
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
    return result 

@shared_task
def reads_snp_analysis(indir,reffile,boot,result,jobid):
    status_file=stautsdir+"/"+jobid+".log.txt"
    line='start at '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.system("echo {line}>{file}".format(line=line,file=status_file)) 
    try:
        cmd="python3 {bind}/10.Reads_snp/run.snp_pipe.py -i {indir} -r {ref} -b {boot} -o {result}".format(bind=bind,indir=indir,ref=reffile,boot=boot,result=result)
        print(cmd)
        os.system(cmd)
        tagfile=result+"/result/all.final.snp.vcf"
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line=''
        if os.path.exists(tagfile) and os.path.getsize(tagfile):
            line='success+['+time1+']'
        else:
            line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file)) 
    except:
        print("发生异常")
        time1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line='fail+['+time1+']'
        os.system("echo {line}>>{file}".format(line=line,file=status_file))
    return result 
   
def celery_send_email(subject, message, from_email, recipient_list, **kwrags):
    try:
        # 使用celery并发处理邮件发送的任务
        logger.info("\n开始发送邮件")
        send_mail(subject, message, from_email, recipient_list, **kwrags)
        logger.info("邮件发送成功")
        return 'success!'
    except Exception as e:
        logger.error("邮件发送失败: {}".format(e))

