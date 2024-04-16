from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Dodo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    alive = models.BooleanField(default=True)
    dead_approved = models.BooleanField(default=False)
    dead_approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_dodos', null=True, blank=True)

    def __str__(self):
        return self.user

class Update(models.Model):
    dodo = models.ForeignKey(Dodo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)