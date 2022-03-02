from django.db import models


class UserDetails(models.Model):
    uniqueID = models.BigAutoField(primary_key=True)
    netID = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=1, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    email_bak = models.CharField(max_length=30, blank=True)
