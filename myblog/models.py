from django.db import models
from django.contrib.auth.models import User
import datetime
from ckeditor.fields import RichTextField

# class Profile(AbstractBaseUser):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     forgot_password_token=models.CharField(max_length=100)
#     # username=models.CharField(max_length=120,unique=True)
#     #created_at=date=models.DateField(auto_now_add=True)

#     # REQUIRED_FIELDS= []
#     # USERNAME_FIELD= 'user'

#     def _str_(self):
#         return self.user.username
    
#     # @property
#     # def is_anonymous(self):
#     #     return False


class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=70,null=True)
    description=RichTextField(blank=True,null=True)
    # description=models.TextField(null=True)
    date=models.DateField(default=datetime.datetime.now)
    author=models.CharField(max_length=70,null=True)
    post_image=models.ImageField(null=True,blank=True)
    likes=models.ManyToManyField(User,related_name='blog_likes')

    def _str_(self):
        return self.user
    
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    body=models.TextField()
    added_date=models.DateField(default=datetime.datetime.now)