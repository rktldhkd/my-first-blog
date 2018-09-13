from django.db import models

# Create your models here.
class Feedback(models.Model):
    id          = models.IntegerField(max_length=5)
    name        = models.CharField(max_length=100)
    email       = models.EmailField()
    comment     = models.TextField(null=False)
    createDate  = models.DateTimeField(auto_now_add=True)