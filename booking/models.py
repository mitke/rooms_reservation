from django.db import models
from django.contrib.auth.models import User

class Rooms(models.Model):
  name = models.CharField(max_length=100)
  capacity = models.IntegerField()
  projector = models.BooleanField()

  def __str__(self):
    return self.name
  

class Bookings(models.Model):
  room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
  user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  organizer_name = models.CharField(max_length=100)
  purpose = models.TextField()
  expected_participants = models.IntegerField()
  needs_projector = models.BooleanField()


class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  telephone_number = models.CharField(max_length=15, blank=True, null=True)
  medical_title = models.CharField(max_length=100, blank=True, null=True)

  def __str__(self):
    return self.user.username
