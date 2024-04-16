from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxLengthValidator



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Dodo(models.Model):
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    alive = models.BooleanField(default=True)
    dead_approved = models.BooleanField(default=False)
    dead_approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_dodos', null=True, blank=True)

    def __str__(self):
        return self.name

class Update(models.Model):
    dodo = models.ForeignKey(Dodo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()


    def __str__(self):
        return self.length          
  
class Time(models.Model):    
    distance = models.ForeignKey(        Distance, on_delete=models.CASCADE, null=False)    
    time_in_minutes = models.IntegerField(
        blank=False,
        validators=[
            MinValueValidator(0, message='Value must be greater or equal to 0'),
            MaxLengthValidator(500, message='Value must be less or equal to 500')
        ])
    date = models.DateField(blank=False,)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    approved = models.BooleanField(default=False)    
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_by', null=True, blank=True)  
      
    def __str__(self):        
        return f"{self.distance.length} by {self.user.get_username()}"

# Create your models here.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
