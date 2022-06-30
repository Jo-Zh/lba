from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from ckeditor.fields import RichTextField


# Create your models here.
class User(AbstractUser):
    is_reader=models.BooleanField(default=False)
    is_poster=models.BooleanField(default=False)
    avatar=models.ImageField(upload_to='media', null=True, blank=True)
    email=models.EmailField(unique=True)
   
    def get_absolute_url(self):
        return reverse('userprofile', args=[self.id])
    

class Category(models.Model):
    name=models.CharField(max_length=100, default='learning-resource', null=True)
    slug=models.SlugField(null=False, unique=True)
    class Meta:
        ordering=('name',)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('home_category', args=[self.slug])


class Posts(models.Model):
    title=models.CharField(max_length=255)
    content=RichTextField(null=True, blank=True)
    cover=models.ImageField(upload_to='media', null=True, blank=True)#
    reader=models.ManyToManyField(User)
    creater= models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    date=models.DateField(auto_now=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    add_like= models.IntegerField(default=0, null=True)
    set_public=models.BooleanField(default=False)
    
    class Meta:
        ordering=('-id',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')


class CommentManager(models.Manager):
    def all(self):
        qs=super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type=ContentType.objects.get_for_model(instance.__class__)
        obj_id=instance.id
        qs=super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs


class Comments(models.Model):
    post=models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments_on')
    parent=models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    name=models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_owner', null=True, blank=True)
    text=models.TextField(null=True, blank=True)
    date=models.DateTimeField(auto_now_add=True)
 
    objects=CommentManager()

    class Meta:
        ordering=['-date']

    def __str__(self):
        return '%s - %s' % (self.name, self.date)

    def get_absolute_url(self):
        return reverse('detail', args=[self.post.id])

    def children(self):
        return Comments.objects.filter(parent=self)
    
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class Notes(models.Model):
    tag=models.CharField(max_length=155, default='default')
    name=models.ForeignKey(User, on_delete=models.CASCADE, related_name='myNote')
    text=models.TextField(null=True, blank=True)
    post=models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='review')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag +"-"+self.name.first_name+"-"+str(self.date)

