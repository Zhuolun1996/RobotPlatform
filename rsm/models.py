from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

#该文件用于描述数据库中存储数据的模型

# Create your models here.

# 容器模型
class server(models.Model):
    # 容器类型
    SERVER_CHOICES = (
        ('Indigo', 'Indigo'),
        ('Kinetic', 'Kinetic'),
        ('Lunar', 'Lunar'),
        ('Linux14', 'Linux14'),
        ('Linux16', 'Linux16')
    )
    # 容器名称
    hostName = models.CharField(max_length=20, null=False, default='No Name', primary_key=True)
    # 容器IP
    hostIP = models.GenericIPAddressField()
    # 容器端口
    hostPort = models.CharField(max_length=5, null=False, default='0')
    # 容器类型
    category = models.CharField(max_length=10, choices=SERVER_CHOICES, null=False, default='Linux16')

    def __str__(self):
        return self.hostName


# 用户信息——拓展User模型
class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    serverNum = models.CharField(max_length=10000, null=False, default='')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


# 文件模型——设定文件存储路径
def upload_to(instance, filename):
    # 文件路径
    return 'files/%s/%s' % (instance.belongTo.username, filename)


# 文件模型
class uploadFile(models.Model):
    # 所属用户
    belongTo = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # 文件
    file = models.FileField(upload_to=upload_to, default='default.txt', null=False, blank=False)
    # 存储的容器
    targetContainer = models.CharField(null=False, default='server0', max_length=20)

    def __str__(self):
        return self.file.name

    # 修改文件路径（在URL中可以传输）
    def getFilePath(self):
        tempFileName = self.file.path.replace('/', '+')
        tempFileName = tempFileName.replace(' ', '=')
        return tempFileName

    # 获取文件名
    def getFileName(self):
        return self.file.name.split('/')[-1]
