from django.db import models
from django.conf import settings


class TheRoom(models.Model):
    title = models.CharField(max_length=255)
    used_by = models.ForeignKey('Session', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.title

    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id

    def set_status(self, status):
        print("models.py setting room new status:", status, "old status", self.in_use)
        self.in_use = status
        self.save()


class Message(models.Model):
    message = models.TextField()
    session = models.ForeignKey('Session', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


class Session(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    key = models.CharField(max_length=100, unique=True)
    in_room = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "%s %s" % (self.key, self.created_at)

    def enter_room(self):
        self.in_room = True
        room = TheRoom.objects.get(id=settings.ROOM_ID)
        room.used_by = self
        room.save()
        self.save()

    def leave_room(self):
        self.in_room = False
        room = TheRoom.objects.get(id=settings.ROOM_ID)
        room.used_by = None
        room.save()
        self.save()

