import datetime
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    email = models.EmailField(null=False,blank=False,unique=True)
    dob = models.DateField(null=False,blank=False)

    def __str__(self):
        return "{} ({})".format(self.name,self.pk)

    def __repr__(self):
        return "{}".format(self.name)

class Student_Subjects(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.IntegerField(null=False,blank=False)
    created_on = models.DateTimeField(default=datetime.datetime.now)
    modified_on = models.DateTimeField(default=None,null=True)

    def __str__(self):
        return "{}->{} ({})".format(self.student,self.subject,self.pk)

    def __repr__(self):
        return "{}->{} ({})".format(self.student,self.subject,self.pk)

    class Meta:
        unique_together = ('student', 'subject',)


