from django.db import models
from django.utils import timezone
# Create your models here.

class PTTPost(models.Model):
    title = models.CharField(max_length=100,null=False,blank=False)
    push = models.CharField(max_length=10,null=False,blank=False)
    date = models.CharField(max_length=10,null=False,blank=False)
    author = models.CharField(max_length=10,null=False,blank=False)
    content = models.TextField(null=False,blank=False)
    times = models.CharField(max_length=20,null=False,blank=False)
    link = models.CharField(max_length=100,null=False,blank=False)
    def __str__(self):
        return self.title

class PTTLink(models.Model):
    link = models.CharField(max_length=50,default='')
    date = models.DateTimeField(default=timezone.now())
    class Meta:
        get_latest_by = 'date'
    def __str__(self):
        return self.link