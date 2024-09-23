from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
  

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username  = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    subject = models.CharField(max_length=200) 
    message = models.TextField()
    
    class Meta:
        verbose_name = "ContactUs"
        verbose_name_plural = "ContactUs"
        

    def __str__(self):
        return self.full_name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.bio}"



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

