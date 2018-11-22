from django.db import models

class Profile(models.Model):
   picture = models.FileField(blank=False, null=False, upload_to='dataset/%Y/%m/%D/')


   class Meta:
      db_table = "profile"
