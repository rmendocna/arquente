from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Base(models.Model):
    creator = models.ForeignKey(User,  editable=False, related_name='%(class)s_creator',)
    created = models.DateTimeField(editable=False)
    modifier = models.ForeignKey(User,  editable=False, related_name='%(class)s_modifier',)
    modified = models.DateTimeField(editable=False)
    
    def save(self, *args,  **kwargs):
        self.modified = datetime.now()
        if not self.created:
            self.created=self.modified
            self.creator=self.modifier
        super(Base, self).save(*args,  **kwargs)
        
