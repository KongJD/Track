# Generated by Django 3.1.5 on 2023-11-27 16:17

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='组织名称', max_length=100, null=True, verbose_name='组织名称')),
                ('function', models.CharField(blank=True, help_text='组织功能', max_length=100, null=True, verbose_name='组织功能')),
                ('contact', models.CharField(blank=True, help_text='联系人', max_length=100, null=True, verbose_name='联系人')),
                ('address', models.CharField(blank=True, help_text='组织地址', max_length=200, null=True, verbose_name='组织地址')),
                ('city', models.CharField(blank=True, help_text='城市', max_length=50, null=True, verbose_name='组织地址')),
                ('country', models.CharField(blank=True, help_text='国家', max_length=50, null=True, verbose_name='国家')),
                ('email', models.EmailField(blank=True, default=None, help_text='邮箱', max_length=254, null=True, verbose_name='邮箱')),
                ('phone', models.CharField(blank=True, help_text='联系方式/电话', max_length=20, null=True, verbose_name='联系方式/电话')),
                ('is_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('roles', models.IntegerField(choices=[[0, 'admin'], [1, 'user'], [2, '采样人']], default=1, verbose_name='角色')),
                ('company', models.CharField(blank=True, help_text='企业名称', max_length=500, verbose_name='企业')),
                ('nickname', models.CharField(blank=True, help_text='昵称', max_length=50, verbose_name='昵称')),
                ('work_number', models.CharField(blank=True, help_text='工号', max_length=10, null=True, verbose_name='工号')),
                ('position', models.CharField(blank=True, help_text='职位', max_length=20, null=True, verbose_name='职位')),
                ('email', models.EmailField(blank=True, default=None, help_text='邮箱', max_length=254, null=True, verbose_name='邮箱')),
                ('phone_number', models.CharField(blank=True, help_text='联系方式/电话', max_length=20, null=True, verbose_name='联系方式/电话')),
                ('organizationId', models.CharField(blank=True, help_text='所属组织', max_length=50, null=True, verbose_name='所属组织')),
                ('last_login', models.DateTimeField(auto_now=True, null=True, verbose_name='last login')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户表自定义',
                'verbose_name_plural': '用户表自定义',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
