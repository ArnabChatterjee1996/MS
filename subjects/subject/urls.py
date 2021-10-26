from django.urls import path

from .views import *

urlpatterns = [

    path('subject/add/', add_subject, name='Add subject'),
    path('subject/get/', get_subject, name='Get subject by id or email'),
    path('subject/all/get/', get_all_subjects, name='Get all subjects'),
    path('subject/update/', update_subject, name='Update subject by id or name'),
    path('student/delete/', delete_subject, name='Delete subject by id or name'),

    path('v1/health', server_health),

]
