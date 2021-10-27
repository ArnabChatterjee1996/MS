import datetime

from django.core.validators import MinValueValidator
from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False,unique=True)
    book_url = models.URLField()
    students_opted = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)

    def __str__(self):
        return "{} ({})".format(self.name,self.pk)

    def __repr__(self):
        return "{}".format(self.name)



