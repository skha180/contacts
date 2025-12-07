from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True, null=True)  # NEW FIELD

    def save(self, *args, **kwargs):
        # Always store name in uppercase
        if self.name:
            self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
