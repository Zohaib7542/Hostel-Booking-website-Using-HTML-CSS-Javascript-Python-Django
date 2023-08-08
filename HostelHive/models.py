from django.db import models

# Create your models here.
class Booknow(models.Model):
    name = models.CharField(max_length=122)
    country_zip = models.CharField(max_length=122)
    checkin = models.DateField()
    checkout = models.DateField()
    rooms = models.CharField(max_length=15, default="1", null=False)
    adults = models.CharField(max_length=15, default="1", null=False)
    children = models.CharField(max_length=15, default="", null=False)
    email = models.EmailField(max_length=15, null=False)
    phonenumber = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.name