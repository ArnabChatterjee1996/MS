from rest_framework import serializers
from .models import Student,Student_Subjects

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Subjects
        fields = '__all__'
