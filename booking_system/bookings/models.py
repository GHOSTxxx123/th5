from django.db import models
from django.contrib.auth.models import User


class Resourse(models.Model):
    name = models.CharField(max_length=100)
    max_slots = models.PositiveIntegerField()
    
    
    def __str__(self):
        return self.name
    
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('queued', 'Queued'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resourse = models.ForeignKey(Resourse, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    
    def __str__(self):
        return f"{self.user.username} - {self.resourse.name} ({self.status})"
    
    
class BookingQueue(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    position = models.PositiveIntegerField() 
    
    
    def __str__(self):
        return f"Queue for {self.booking.resourse.name} - Position: {self.position}"

    
    
    