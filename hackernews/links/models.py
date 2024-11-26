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
        posted_by(ForeignKey): A reference to the User who posted the link, with a cascading delete behavior.
    """
    url=models.URLField()
    description=models.TextField(blank=True)
    posted_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    
class Vote(models.Model):
    """
    Vote is a Django model that represents a user's vote on a specific link. 
    It establishes relationships between users and links, allowing for the tracking of votes associated with each link.

    Attributes:
        user (ForeignKey): A reference to the User who cast the vote, with a cascading delete behavior.
        link (ForeignKey): A reference to the Links model, indicating which link the vote is associated with, with a related name for reverse access to votes.
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    link = models.ForeignKey(Links,related_name="votes",on_delete=models.CASCADE)
