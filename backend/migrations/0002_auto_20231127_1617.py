# Generated by Django 3.1.5 on 2023-11-27 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfq',
            name='usern',
            field=models.ForeignKey(help_text='用户名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='tasklist',
            name='usern',
            field=models.ForeignKey(help_text='用户名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='straininfo',
            name='sampleNo',
            field=models.ForeignKey(help_text='采样样品编号', on_delete=django.db.models.deletion.CASCADE, to='backend.sampling', to_field='sampleNo', verbose_name='采样样品编号'),
        ),
        migrations.AddField(
            model_name='straininfo',
            name='usern',
            field=models.ForeignKey(help_text='用户名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='sequencing',
            name='usern',
            field=models.ForeignKey(help_text='用户名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='sampling',
            name='usern',
            field=models.ForeignKey(help_text='用户名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='pipelinesample',
            name='usern',
            field=models.ForeignKey(help_text='用户名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='multi_upload',
            name='usern',
            field=models.ForeignKey(help_text='用户名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='multi_fasta',
            name='usern',
            field=models.ForeignKey(help_text='用户名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='jobstat',
            name='usern',
            field=models.ForeignKey(help_text='用户名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='job2task',
            name='usern',
            field=models.ForeignKey(help_text='用户名', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
    ]
