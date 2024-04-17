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
    dodo = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
    date_of_birth = models.DateField(null=True, blank=True)
    alive = models.BooleanField(default=True)
    dead_approved = models.BooleanField(default=False)
    dead_approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_dodos', null=True, blank=True)

    def __str__(self):
        return f"{self.dodo} - Added by {self.user.username}"


class Update(models.Model):
    dodo = models.ForeignKey(Dodo, on_delete=models.CASCADE, related_name='updates')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"Update for {self.dodo.dodo} - Added by {self.user.username} on {self.date}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)