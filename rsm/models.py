from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class server(models.Model):
    hostName = models.CharField(max_length=20, null=False, default='No Name', primary_key=True)
    hostIP = models.GenericIPAddressField()
    hostPort = models.CharField(max_length=5, null=False, default='0')

    def __str__(self):
        return self.hostName


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


class course(models.Model):
    courseName = models.CharField(max_length=100, null=False, primary_key=True)
