from __future__ import unicode_literals

from django.db import models

# Create your models here.

class url_original(models.Model):
	url = models.TextField(default = "")