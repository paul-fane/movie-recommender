# from django.conf import settings
# from django.db import models

# User = settings.AUTH_USER_MODEL # "auth.User"


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True, null=True)
#     location = models.CharField(max_length=100, blank=True, null=True)
#     #avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

#     def __str__(self):
#         return self.user.username