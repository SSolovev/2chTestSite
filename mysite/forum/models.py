from django.db import models

class Categories(models.Model):
    category = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    auth_required = models.BooleanField(default = False)

    def __unicode__(self):
        return self.category


class Subcategories(models.Model):
    subcategory = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Categories)
    auth_required = models.BooleanField(default = False)

    def __unicode__(self):
        return self.subcategory


class Topics(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    creator_name = models.CharField(max_length=10)
    subcategory = models.ForeignKey(Subcategories)
    update_date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=100,blank=True)

    def __unicode__(self):
        return self.title


class Messages(models.Model):
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    creator_name = models.CharField(max_length=10)
    topic = models.ForeignKey(Topics)
    file_name = models.CharField(max_length=100,blank=True)

    def __unicode__(self):
        return self.creator_name+" : "+self.topic.title +" : "+ str(self.id)

    class Meta:
     ordering = ('-date',)

# Create your models here.
