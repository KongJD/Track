from django.db import models
from django.conf import settings
# Create your models here.


class ModelManager(models.Manager):
    # 重写get_queryset方法
    def get_queryset(self):
        # 查询出所有的数据，但是不包括软删除的数据
        return super().get_queryset().filter(is_delete=False)
class ModelAdminManager(models.Manager):
    pass
    


class BaseModel(models.Model):
    # 是否删除
    is_delete = models.BooleanField(default=False)
    # 注册时间，首次登录，插入当前时间，后面基本不会变
    create_time = models.DateTimeField(auto_now_add=True)
    # 只要更新，就插入当前时间
    updated_time = models.DateTimeField(auto_now=True)
    class Meta:
        #联合索引、联合唯一（ip和端口）
        abstract=True
        #抽象表，不然每个继承的它的类都会生成一个表
        


##采样表
class Sampling(BaseModel): 
    #id = models.AutoField(primary_key=True, editable=False)
    usern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text="用户名",verbose_name="用户名")
    receiver=models.CharField(max_length=100,verbose_name="收样人",null=True,blank=True,help_text="收样人")
    labName=models.CharField(max_length=100,verbose_name="项目名称",null=True,blank=True,help_text="项目名称")
    project=models.CharField(max_length=100,verbose_name="样品收集实验室名称",null=True,blank=True,help_text="样品收集实验室名称")
    sampleNo=models.CharField(max_length=100,verbose_name="采样样品编号",null=True,blank=True,help_text="采样样品编号",unique=True)
    collectionTime=models.CharField(max_length=50,verbose_name="样品收集时间",blank=True,null=True,help_text="样品收集时间")
    sourceType=models.CharField(max_length=50,verbose_name="样品来源",blank=True,null=True,help_text="样品来源")
    productName=models.CharField(max_length=100,verbose_name="产品名称",blank=True,null=True,help_text="产品名称")
    processLink=models.CharField(max_length=100,verbose_name="加工环节",blank=True,null=True,help_text="加工环节")
    envMaterials=models.CharField(max_length=100,verbose_name="环境材料",blank=True,null=True,help_text="环境材料")
    envLocation=models.CharField(max_length=100,verbose_name="环境位置",blank=True,null=True,help_text="环境位置")
    collectionDevice=models.CharField(max_length=100,verbose_name="收集装置",blank=True,null=True,help_text="收集装置")
    collectionMethod=models.CharField(max_length=100,verbose_name="收集方法",blank=True,null=True,help_text="收集方法")
    organizationId=models.IntegerField(null=True, blank=True,verbose_name="组织id",help_text="组织id")
    city=models.CharField(max_length=50,verbose_name="城市",blank=True,null=True,help_text="城市")
    province=models.CharField(max_length=50,verbose_name="省份",blank=True,null=True,help_text="省份")
    country=models.CharField(max_length=50,verbose_name="国家",blank=True,null=True,help_text="国家")
    beiDou=models.CharField(max_length=100,verbose_name="北斗",blank=True,null=True,help_text="北斗")    
    location=models.CharField(max_length=100,verbose_name="经纬度",blank=True,null=True,help_text="经纬度")
    create_userid=models.IntegerField(null=True, blank=True,verbose_name="创建用户id",help_text="创建用户id")
    update_userid=models.IntegerField(null=True, blank=True,verbose_name="更新用户id",help_text="更新用户id")
    remarks=models.CharField(max_length=250,verbose_name="备注",blank=True,null=True)

    #@property
    #def sid(self):
    #    return "DMS%05d" % self.id
        
    class Meta:
        verbose_name = "采样信息表"
        verbose_name_plural = verbose_name
        ordering = ['-create_time', '-updated_time']
    # 替换默认的objects
    objects = ModelManager()
    objects_all = ModelAdminManager()


##菌株信息管理表

class StrainInfo(BaseModel): 
    #id = models.AutoField(primary_key=True, editable=False)
    usern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text="用户名",verbose_name="用户名")
    expOperator = models.CharField(max_length=100,null=True,blank=True,help_text="微生物实验操作员",verbose_name="微生物实验操作员")
    strainId=models.CharField(max_length=100,verbose_name="菌株编号",null=True,blank=True,help_text="菌株编号")
    isolateNo=models.CharField(max_length=100,verbose_name="Isolate编号",null=True,blank=True,help_text="Isolate编号")
    sampleNo=models.ForeignKey('Sampling', to_field='sampleNo', on_delete=models.CASCADE,help_text="采样样品编号",verbose_name="采样样品编号")
    separationTime=models.CharField(max_length=100,verbose_name="分离时间",null=True,blank=True,help_text="分离时间")
    identificationResult=models.CharField(max_length=200,verbose_name="其他平台鉴定结果",blank=True,null=True,help_text="其他平台鉴定结果")
    identificationMethod=models.CharField(max_length=200,verbose_name="鉴定方法",blank=True,null=True,help_text="鉴定方法")
    serotype =models.CharField(max_length=100,verbose_name="血清型",blank=True,null=True,help_text="血清型")
    sp_medium=models.CharField(max_length=200,verbose_name="培养基",blank=True,null=True,help_text="培养基")
    sp_temperature=models.CharField(max_length=100,verbose_name="培养温度",blank=True,null=True,help_text="培养温度")
    sp_oxygen=models.CharField(max_length=100,verbose_name="氧气需求",blank=True,null=True,help_text="氧气需求")
    sp_cultureCycle=models.CharField(max_length=100,verbose_name="培养周期",blank=True,null=True,help_text="培养周期")
    generation=models.CharField(max_length=100,verbose_name="传代次数",blank=True,null=True,help_text="传代次数")
    geneMethod=models.CharField(max_length=100,verbose_name="传代方法",blank=True,null=True,help_text="传代方法")
    antibioticName=models.CharField(max_length=100,verbose_name="抗生素名称",blank=True,null=True,help_text="抗生素名称")
    micZoi=models.CharField(max_length=100,verbose_name="MIC值/ZOI值",blank=True,null=True,help_text="MIC值/ZOI值")
    pesistance=models.CharField(max_length=100,verbose_name="抗性表型",blank=True,null=True,help_text="抗性表型")
    ar_testMethod=models.CharField(max_length=100,verbose_name="测试方法（抗生素）",blank=True,null=True,help_text="测试方法（抗生素）")
    ar_testStandard=models.CharField(max_length=100,verbose_name="测试标准（抗生素）",blank=True,null=True,help_text="测试标准（抗生素）")
    ar_testPlatform=models.CharField(max_length=100,verbose_name="测试平台（抗生素）",blank=True,null=True,help_text="测试平台（抗生素）")
    ar_remarks=models.CharField(max_length=100,verbose_name="备注（抗菌谱）",blank=True,null=True,help_text="备注（抗菌谱）")
    vf_name=models.CharField(max_length=50,verbose_name="毒力因子名称",blank=True,null=True,help_text="毒力因子名称")
    vf_testMethod=models.CharField(max_length=50,verbose_name="毒力因子检测方法",blank=True,null=True,help_text="毒力因子检测方法")
    insperctionLimit=models.CharField(max_length=50,verbose_name="毒力因子检测限度",blank=True,null=True,help_text="毒力因子检测限度")
    colonyMorpholob=models.CharField(max_length=200,verbose_name="菌落形态",blank=True,null=True,help_text="菌落形态")
    phyandMio=models.CharField(max_length=200,verbose_name="生理生化",blank=True,null=True,help_text="生理生化")
    remarks=models.CharField(max_length=250,verbose_name="备注",blank=True,null=True)
    organizationId=models.IntegerField(null=True, blank=True,verbose_name="组织id",help_text="组织id")
    create_userid=models.IntegerField(null=True, blank=True,verbose_name="创建用户id",help_text="创建用户id")
    update_userid=models.IntegerField(null=True, blank=True,verbose_name="更新用户id",help_text="更新用户id")
    #@property
    #def sid(self):
    #    return "DM%05d" % self.id
        
    class Meta:
        verbose_name = "菌株信息管理表"
        verbose_name_plural = verbose_name
        ordering = ['-create_time', '-updated_time']
    # 替换默认的objects
    objects = ModelManager()
    objects_all = ModelAdminManager()
    
    
    
##测序实验信息管理表
  
class Sequencing(BaseModel): 
    #id = models.AutoField(primary_key=True, editable=False)
    usern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text="用户名",verbose_name="用户名")
    seqNo=models.CharField(max_length=100,null=True,blank=True,help_text="测序样品编号",verbose_name="测序样品编号")
    sequencer = models.CharField(max_length=100,null=True,blank=True,help_text="测序人",verbose_name="测序人")
    seq_date=models.DateField(null=True,help_text="测序日期",verbose_name="测序日期")
    strainId=models.CharField(max_length=100,verbose_name="菌株编号",null=True,blank=True,help_text="菌株编号")
    sampleName=models.CharField(max_length=100,null=True,blank=True,help_text="样品名称",verbose_name="样品名称")
    DNA_kitName=models.CharField(max_length=100,null=True,blank=True,help_text="试剂盒名称",verbose_name="试剂盒名称")
    DNA_batch=models.CharField(max_length=10,verbose_name="DNA批次号",null=True,blank=True,help_text="DNA批次号")
    DNA_labProtocol=models.CharField(max_length=200,verbose_name="DNA实验室protocol",blank=True,null=True,help_text="DNA实验室protocol")
    DNA_nongdu=models.CharField(max_length=50,verbose_name="DNA浓度",blank=True,null=True,help_text="DNA浓度")
    DNA_q=models.CharField(max_length=50,verbose_name="DNA质量",blank=True,null=True,help_text="DNA质量")
    DNA_qc =models.CharField(max_length=100,verbose_name="A260/A280",blank=True,null=True,help_text="A260/A280")
    qualityRate=models.CharField(max_length=100,verbose_name="质量评级",blank=True,null=True,help_text="质量评级")
    seq_batch=models.CharField(max_length=100,verbose_name="测序批次",blank=True,null=True,help_text="测序批次")
    repetitionType=models.CharField(max_length=100,verbose_name="重复类型",blank=True,null=True,help_text="重复类型")
    wenku_kitName=models.CharField(max_length=100,verbose_name="试剂盒名称（文库）",blank=True,null=True,help_text="试剂盒名称（文库）")
    wenku_batch=models.CharField(max_length=100,verbose_name="批次号（文库）",blank=True,null=True,help_text="批次号（文库）")
    wenku_labProtocol=models.CharField(max_length=100,verbose_name="批次号（文库）",blank=True,null=True,help_text="批次号（文库）")
    adapter=models.CharField(max_length=100,verbose_name="接头信息",blank=True,null=True,help_text="接头信息")
    wenku_name=models.CharField(max_length=100,verbose_name="文库编号",blank=True,null=True,help_text="文库编号")
    wenku_nongdu=models.CharField(max_length=100,verbose_name="浓度（文库质量）",blank=True,null=True,help_text="浓度（文库质量）")
    wenku_size=models.CharField(max_length=50,verbose_name="文库片段大小",blank=True,null=True,help_text="文库片段大小")
    seq_platform=models.CharField(max_length=50,verbose_name="测序平台",blank=True,null=True,help_text="测序平台")
    platform_type=models.CharField(max_length=50,verbose_name="平台类型",blank=True,null=True,help_text="平台类型")
    seq_celue=models.CharField(max_length=50,verbose_name="测序策略",blank=True,null=True,help_text="测序策略")
    filename=models.CharField(max_length=1000,verbose_name="文件名称",blank=True,null=True,help_text="文件名称")
    filelink=models.CharField(max_length=1000,verbose_name="文件保存位置",blank=True,null=True,help_text="文件保存位置")
    analyticalLab=models.CharField(max_length=100,verbose_name="分析实验室",blank=True,null=True,help_text="分析实验室")
    analyticalPerson=models.CharField(max_length=50,verbose_name="分析人",blank=True,null=True,help_text="分析人")
    rawData=models.CharField(max_length=1000,verbose_name="测序原始数据处理",blank=True,null=True,help_text="测序原始数据处理")
    filterMethod=models.CharField(max_length=500,verbose_name="测序数据过滤方法",blank=True,null=True,help_text="测序数据过滤方法")
    assemblyMethod=models.CharField(max_length=200,verbose_name="序列组装方法",blank=True,null=True,help_text="序列组装方法")
    annotationMethod=models.CharField(max_length=200,verbose_name="序列注释方法",blank=True,null=True,help_text="序列注释方法")
    qualityMatrix=models.CharField(max_length=200,verbose_name="序列组装质量矩阵",blank=True,null=True,help_text="序列组装质量矩阵")   
    remarks=models.CharField(max_length=250,verbose_name="备注",blank=True,null=True)
    organizationId=models.IntegerField(null=True, blank=True,verbose_name="组织id",help_text="组织id")
    create_userid=models.IntegerField(null=True, blank=True,verbose_name="创建用户id",help_text="创建用户id")
    update_userid=models.IntegerField(null=True, blank=True,verbose_name="更新用户id",help_text="更新用户id")

    #@property
    #def sid(self):
    #    return "DMS%05d" % self.id
        
    class Meta:
        verbose_name = "测序实验信息表"
        verbose_name_plural = verbose_name
        ordering = ['-create_time', '-updated_time']
    # 替换默认的objects
    objects = ModelManager()
    objects_all = ModelAdminManager()
        

class Tasklist(models.Model):
    usern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text="用户名",verbose_name="用户名")
    jobid=models.CharField(max_length=50,verbose_name="任务编号")
    strain=models.CharField(max_length=100,verbose_name="菌株编号")
    sampleName=models.CharField(max_length=100,verbose_name="样品名称",null=True, blank=True)
    Seq_platform  =models.CharField(max_length=200,verbose_name="测序平台",null=True, blank=True)
    library=models.CharField(max_length=100,verbose_name="文库编号",null=True, blank=True)
    datanum=models.CharField(max_length=200,verbose_name="数据量",null=True, blank=True)
    protocol=models.CharField(max_length=50,verbose_name="任务类别",null=True, blank=True)
    tag=models.CharField(max_length=50,verbose_name="工具分类",null=True, blank=True)
    stauts=models.CharField(max_length=50,verbose_name="任务状态",null=True, blank=True)
    submit_date=models.CharField(max_length=50,verbose_name="提交时间",blank=True)
    complete_date=models.CharField(max_length=50,verbose_name="完成时间",blank=True)
    result=models.CharField(max_length=100,verbose_name="结果信息",blank=True)
    create_date=models.DateTimeField(auto_now =True,verbose_name="创建时间")


class pipelineSample(models.Model):
    usern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text="用户名",verbose_name="用户名")
    jobID = models.CharField(max_length=50,verbose_name="任务编号")
    strain=models.CharField(max_length=100,verbose_name="菌株编号")
    sampleName=models.CharField(max_length=100,verbose_name="样品名称",blank=True)
    create_date=models.DateTimeField(auto_now =True)
    

class Uploadfq(models.Model):
    usern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text="用户名",verbose_name="用户名")
    strain=models.CharField(max_length=100,verbose_name="菌株编号")
    sampleName=models.CharField(max_length=100,verbose_name="样品名称",blank=True)
    library=models.CharField(max_length=100,verbose_name="文库编号",blank=True)
    Seq_platform=models.CharField(max_length=200,verbose_name="测序平台",blank=True)
    Seq_batch=models.IntegerField(default=1,verbose_name="测序批次",blank=True)
    platform_type =models.CharField(max_length=200,verbose_name="平台类型",blank=True)
    filepath=models.CharField(max_length=1000,verbose_name="fastq路径",blank=True)
    filename=models.CharField(max_length=2000,verbose_name="fastq名称",blank=True)
    create_date=models.DateTimeField(auto_now =True,verbose_name="创建时间")

class Multi_Upload(models.Model):
    usern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text="用户名",verbose_name="用户名")
    jobID = models.CharField(primary_key=True,max_length=30)
    path=models.CharField(max_length=4000)
    filename=models.CharField(max_length=2000)
    tasktype=models.CharField(max_length=100)
    marker=models.CharField(max_length=100,null=True)
    email=models.EmailField()
    upload_date=models.DateTimeField(auto_now_add =True)
    def __str__(self):
        return self.jobID

class Multi_Fasta(models.Model):
    usern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text="用户名",verbose_name="用户名")
    path=models.CharField(max_length=4000,verbose_name="fasta路径",blank=True)
    filename=models.CharField(max_length=2000,verbose_name="fasta路径",blank=True)
    upload_date=models.DateTimeField(auto_now_add =True)
    def __str__(self):
        return self.jobID

class JobStat(models.Model):
    usern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text="用户名",verbose_name="用户名")
    jobID = models.CharField(primary_key=True,max_length=30)
    celery_task_id=models.CharField(max_length=100)
    create_date=models.DateTimeField(auto_now_add =True)

    def __str__(self):
        return self.celery_task_id


class Job2Task(models.Model):
    usern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,help_text="用户名",verbose_name="用户名")
    jobID=models.CharField(primary_key=True,max_length=30)
    task_name=models.CharField(max_length=80)
    email=models.EmailField(null=True,default=None)
    create_date=models.DateTimeField(auto_now_add =True)
    def __str__(self):
        return self.jobID


