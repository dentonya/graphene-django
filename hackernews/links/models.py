from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Links(models.Model):
    """Represents a link with a URL and an optional description.

    This model is used to store links along with their descriptions. The URL is a required field, while the description can be left blank.
    
    Attributes:
        url (URLField): The URL of the link.
        description (TextField): An optional description of the link.
    """
    url=models.URLField()
    description=models.TextField(blank=True)
    posted_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
