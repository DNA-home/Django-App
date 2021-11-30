from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE,SET_NULL



# Create your models here.



class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name






class Room(models.Model):
    """the host field is there to make the relationship between room and topic one to many, I don't know how.
    but if I had to guess I think the host field relates the room to a host which is a user in a many to one relationship.
    the topic field relates the room entity to the topic entity"""

    host= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
    participants=models.ManyToManyField(User,related_name='participants', blank='true')
    # id=models.UUIDField(primary_key=True)



    #this is for date of creation and date of updation
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-updated','-created']


    def __str__(self):
        return str(self.name)




class Message(models.Model):
    """the user field is there to make the relationship one to many, I think the concept behind it is that a User can have many
    messages, and this sort of relates the user to the message
    The room field is there to relate the messages and the 
    room entities or tables"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    room =models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()

    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-updated','-created']


    def __str__(self):
        return self.body[:50]