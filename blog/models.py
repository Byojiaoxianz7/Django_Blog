from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import ReadNumExpendMethon, ReadDetail



class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model, ReadNumExpendMethon):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING) # 文章类型
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']







