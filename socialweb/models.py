from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)
    description=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True)
    like=models.ManyToManyField(User,related_name="posts")

    class Meta:
        ordering=["-created_date"]

    def __str__(self):
        return self.title
    
    @property
    def like_count(self):
        return self.like.all().count()
    @property
    def post_comment(self):
        return Comments.objects.filter(post=self).annotate(ucount=Count('likes')).order_by('-ucount')

class UserProfile(models.Model):
    profile_pic=models.ImageField(upload_to="images",null=True)
    bio=models.CharField(max_length=200)
    timeline_pic=models.ImageField(upload_to="images",null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_active=models.BooleanField(default=True)

    @property
    def Post_count(self):
        return Post.objects.filter(user=self.user).count()
    
class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.CharField(max_length=300,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name="comment")
    class Meta:
        ordering=["-created_date"]
    def __str__(self):
        return self.post
    @property
    def like_count(self):
        return self.likes.all().count()
    