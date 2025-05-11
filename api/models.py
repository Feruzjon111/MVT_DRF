from django.db import models


class OTP(models.Model):
    phone = models.CharField(max_length=12)
    key = models.CharField(max_length=100)
    is_expire = models.BooleanField(default=False)
    is_conf = models.BooleanField(default=False)
    tried = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.tried >= 3:
            self.is_expire = True
        super(OTP, self).save(*args, **kwargs)
