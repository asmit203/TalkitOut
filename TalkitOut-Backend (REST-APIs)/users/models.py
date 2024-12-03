from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
            ('standard', 'Standard User'),
            ('privilaged', 'Privilged User'),
            ('admin', 'Administrator')
        ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    lastseen = models.DateTimeField(default=timezone.now)  # Add lastseen field here
    is_verified = models.BooleanField(default=False)  # Add verification field
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='standard') # Add role field
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height>300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
    # models.py - add to Profile class
    def is_admin(self):
        return self.role == 'admin'

    def is_doctor(self):
        return self.role == 'privilaged'

    def is_standard(self):
        return self.role == 'standard'

    def can_access_admin_panel(self):
        return self.is_admin()

    def can_view_patient_records(self):
        return self.is_admin() or self.is_doctor()