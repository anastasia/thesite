from django.db import models

class TheRoom(models.Model):
    title = models.CharField(max_length=255)
    in_use = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id

class Message(models.Model):
    message = models.TextField()
    session_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
