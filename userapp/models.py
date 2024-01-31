from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.conf import settings

# Create your models here.


class NewUser(AbstractUser):

    role_type = [
        [0, 'admin'],
        [1, 'user'],
        [2,'采样人']
    ]
    roles = models.IntegerField(verbose_name='角色', choices=role_type, default=1)
    company = models.CharField(max_length=500, blank=True,help_text="企业名称",verbose_name="企业")
    nickname=models.CharField(max_length=50, blank=True,help_text="昵称",verbose_name="昵称")
    work_number=models.CharField(max_length=10,null=True, blank=True,help_text="工号",verbose_name="工号")
    position=models.CharField(max_length=20,null=True, blank=True,help_text="职位",verbose_name="职位")
    email=models.EmailField(null=True,blank=True,default=None,help_text="邮箱",verbose_name="邮箱")
    phone_number=models.CharField(max_length=20,null=True,blank=True,help_text="联系方式/电话",verbose_name="联系方式/电话")
    organizationId=models.CharField(max_length=50,null=True,blank=True,help_text="所属组织",verbose_name="所属组织")
    last_login = models.DateTimeField('last login', blank=True, null=True, auto_now=True)
    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = "用户表自定义"
        verbose_name_plural = verbose_name
        pass


class Organization(models.Model):##组织
    name=models.CharField(max_length=100, blank=True,null=True,help_text="组织名称",verbose_name="组织名称")
    function=models.CharField(max_length=100, blank=True,null=True,help_text="组织功能",verbose_name="组织功能")
    contact=models.CharField(max_length=100, blank=True,null=True,help_text="联系人",verbose_name="联系人")
    address=models.CharField(max_length=200, blank=True,null=True,help_text="组织地址",verbose_name="组织地址")
    city=models.CharField(max_length=50, blank=True,null=True,help_text="城市",verbose_name="组织地址")
    country=models.CharField(max_length=50, blank=True,null=True,help_text="国家",verbose_name="国家")
    email=models.EmailField(null=True,blank=True,default=None,help_text="邮箱",verbose_name="邮箱")
    phone=models.CharField(max_length=20,null=True,blank=True,help_text="联系方式/电话",verbose_name="联系方式/电话")
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    # 只要更新，就插入当前时间
    updated_time = models.DateTimeField(auto_now=True)