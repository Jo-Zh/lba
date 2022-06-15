from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

# Create your models here.
class User(AbstractUser):
    is_reader=models.BooleanField(default=False)
    is_poster=models.BooleanField(default=False)
    avatar=models.ImageField(upload_to='media', null=True, blank=True)
    
    # IMAGE_MAX_SIZE=(150, 150)

    # def resize_image(self):
    #     image=Image.open(self.avatar)
    #     image.thumbnail(self.IMAGE_MAX_SIZE)
    #     image.save(self.avatar.path)
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.resize_image()




class Posts(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField(null=True, blank=True)
    cover=models.ImageField(upload_to='media', null=True, blank=True)
    reader=models.ManyToManyField(User)
    creater= models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

