from django.urls import path

from .views import *

urlpatterns = [

    path('student/add/', add_student, name='Add student'),
    path('student/get/', get_student, name='Get student by id or email'),
    path('student/update/', update_student, name='Update student by id or email'),
    path('student/delete/', delete_student, name='Delete student by id or email'),
    path('student/subject/add/', add_student_to_subject, name='Add subject(name or id) to a student(email or id)'),
    path('student/subject/remove/', remove_subject_from_student,
         name='Remove subject(name or id) from a student(email or id)'),
    path('student/subject/get/', get_subject_for_student, name='Get subject details for a student(email or id)'),

    path('v1/health', server_health),

]
