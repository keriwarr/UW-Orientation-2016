import datetime

from django.db import models


class Announcement(models.Model):
    """
    Represents an announcement.
    """
    title = models.CharField(max_length=100, blank=False)
    text = models.TextField(blank=False)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        """
        On save, update timestamps.
        """
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(Announcement, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
