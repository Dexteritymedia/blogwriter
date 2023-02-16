from django.db import models

# Create your models here.

class AdCopy(models.Model):

    STATUS = (
        ('Sent', 'Sent'),
        ('Pending', 'Pending'),
    )
    
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    product = models.CharField(max_length=150, blank=True)
    ad_copy = models.TextField(blank=True)
    description = models.CharField(max_length=150, blank=True)
    status = models.CharField(choices=STATUS, max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
