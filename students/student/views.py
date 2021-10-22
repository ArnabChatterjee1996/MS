import random

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from students.logging import logging
from .serializers import *
from .models import Student


@api_view(['GET'])
def server_health(request):
    return Response({"health_status": "OK"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_student(request):
    try:
        logging.info("Entering method add_student with request data : {}".format(request.data))
        serialized_data = StudentSerializer(data=request.data)
        if serialized_data.is_valid():
            logging.info(
                "Starting db transaction for method add_student . Data : {}".format(serialized_data.validated_data))
            serialized_data.save()
            logging.info("Exiting db transaction for method add_student. Data : {}".format(serialized_data.data))
            return Response({"status": "Success",
                             "message": "Student added Successfully",
                             "data": "{}".format(serialized_data.data)},
                            status=status.HTTP_201_CREATED)

        else:
            logging.error("Serializer errors : {}".format(serialized_data.errors))
            return Response({"status": "Failure",
                             "message": "Serializer Errors",
                             "data": "{}".format(serialized_data.errors)},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error("Some error occurred in method : add_student. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_student(request):
    try:
        logging.info("Entering method get_student")
        id = request.GET.get('id')
        email = request.GET.get('email')
        if id is None:
            if email is None:
                logging.error("id and email are both null for request . Params : {}".format(request.GET))
                return Response({"status": "Failure",
                                 "message": "Unable to retrieve data because id and email are both null",
                                 "data": {}},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    logging.info("Entering db for method get_student with id : {} and email : {}".format(id, email))
                    student_data = Student.objects.get(email=email)
                    logging.info(
                        "Exiting db for method get_student with id : {} and email : {} with data : {}".format(id, email,
                                                                                                              student_data))
                except ObjectDoesNotExist:
                    return Response({"status": "Failure",
                                     "message": "Unable to get student because student does not exist",
                                     "data": {}},
                                    status=status.HTTP_404_NOT_FOUND)
                serialized_data = StudentSerializer(student_data)
                return Response({"status": "Success",
                                 "message": "Student data retrieved successfully",
                                 "data": serialized_data.data},
                                status=status.HTTP_200_OK)
        else:
            try:
                logging.info("Entering db for method get_student with id : {} and email : {}".format(id, email))
                student_data = Student.objects.get(pk=id)
                logging.info(
                    "Exiting db for method get_student with id : {} and email : {} with data : {}".format(id, email,
                                                                                                          student_data))
            except ObjectDoesNotExist:
                return Response({"status": "Failure",
                                 "message": "Unable to get student because student does not exist",
                                 "data": {}},
                                status=status.HTTP_404_NOT_FOUND)

            serialized_data = StudentSerializer(student_data)
            return Response({"status": "Success",
                             "message": "Student data retrieved successfully",
                             "data": serialized_data.data},
                            status=status.HTTP_200_OK)

    except Exception as e:
        logging.error("Some error occurred in method : get_student. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_student(request):
    try:
        logging.info("Entering method update_student")
        id = request.GET.get('id')
        email = request.GET.get('email')
        if id is None:
            if email is None:
                logging.error(
                    "id and email are both null for request {}. params : {}".format(request.data, request.GET))
                return Response({"status": "Failure",
                                 "message": "Unable to retrieve data because id and email are both null",
                                 "data": {}},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    logging.info("Entering db for method update_student with id : {} and email : {}".format(id, email))
                    student_data = Student.objects.get(email=email)
                    logging.info(
                        "Exiting db for method update_student with id : {} and email : {} with data : {}".format(id,
                                                                                                                 email,
                                                                                                                 student_data))
                except ObjectDoesNotExist:
                    return Response({"status": "Failure",
                                     "message": "Unable to update student because student does not exist",
                                     "data": {}},
                                    status=status.HTTP_404_NOT_FOUND)
                serialized_data = StudentSerializer(student_data, data=request.data)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return Response({"status": "Success",
                                     "message": "Student data updated successfully",
                                     "data": serialized_data.data},
                                    status=status.HTTP_200_OK)
                else:
                    logging.error("Serializer errors : {}".format(serialized_data.errors))
                    return Response({"status": "Failure",
                                     "message": "Serializer Errors",
                                     "data": "{}".format(serialized_data.errors)},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                logging.info("Entering db for method update_student with id : {} and email : {}".format(id, email))
                student_data = Student.objects.get(pk=id)
                logging.info(
                    "Exiting db for method update_student with id : {} and email : {} with data : {}".format(id, email,
                                                                                                             student_data))
            except ObjectDoesNotExist:
                return Response({"status": "Failure",
                                 "message": "Unable to update student because student does not exist",
                                 "data": {}},
                                status=status.HTTP_404_NOT_FOUND)
            serialized_data = StudentSerializer(student_data, data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({"status": "Success",
                                 "message": "Student data updated successfully",
                                 "data": serialized_data.data},
                                status=status.HTTP_200_OK)
            else:
                logging.error("Serializer errors : {}".format(serialized_data.errors))
                return Response({"status": "Failure",
                                 "message": "Serializer Errors",
                                 "data": "{}".format(serialized_data.errors)},
                                status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logging.error("Some error occurred in method : update_student. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_student(request):
    try:
        logging.info("Entering method delete_student")
        id = request.GET.get('id')
        email = request.GET.get('email')
        if id is None:
            if email is None:
                logging.error(
                    "id and email are both null for request {}. params : {}".format(request.data, request.GET))
                return Response({"status": "Failure",
                                 "message": "Unable to retrieve data because id and email are both null",
                                 "data": {}},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    logging.info("Entering db for method delete_student with id : {} and email : {}".format(id, email))
                    student_data = Student.objects.get(email=email)
                    logging.info(
                        "Exiting db for method delete_student with id : {} and email : {} with data : {}".format(id,
                                                                                                                 email,
                                                                                                                 student_data))
                except ObjectDoesNotExist:
                    return Response({"status": "Failure",
                                     "message": "Unable to delete student because student does not exist",
                                     "data": {}},
                                    status=status.HTTP_404_NOT_FOUND)

                student_data.delete()
                return Response({"status": "Success",
                                 "message": "Student deleted successfully",
                                 "data": {}},
                                status=status.HTTP_200_OK)


        else:
            logging.info("Entering db for method delete_student with id : {} and email : {}".format(id, email))
            try:
                logging.info("Entering db for method delete_student with id : {} and email : {}".format(id, email))
                student_data = Student.objects.get(pk=id)
                logging.info(
                    "Exiting db for method delete_student with id : {} and email : {} with data : {}".format(id,
                                                                                                             email,
                                                                                                             student_data))
            except ObjectDoesNotExist:
                return Response({"status": "Failure",
                                 "message": "Unable to delete student because student does not exist",
                                 "data": {}},
                                status=status.HTTP_404_NOT_FOUND)
            student_data.delete()
            return Response({"status": "Success",
                             "message": "Student deleted successfully",
                             "data": {}},
                            status=status.HTTP_200_OK)

    except Exception as e:
        logging.error("Some error occurred in method : delete_student. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_student_to_subject(request):
    try:
        logging.info("Entering method add_student_to_subject with request data : {}".format(request.data))
        student_id = request.data.get('student_id')
        student_email = request.data.get('student_email')
        subject_name = request.data.get('subject_name')
        subject_id = request.data.get('subject_id')

        ## Get the student details
        if student_id is None:
            if student_email is None:
                logging.error(
                    "student_id and student_email are both null for request {}. params : {}".format(request.data,
                                                                                                    request.GET))
                return Response({"status": "Failure",
                                 "message": "Unable to retrieve student data because student_id and student_email are both null",
                                 "data": {}},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                logging.info("Entering db for method update_student with id : {} and email : {}".format(student_id,
                                                                                                        student_email))
                student_data = Student.objects.get(email=student_email)
                logging.info(
                    "Exiting db for method add_student_to_subject with id : {} and email : {} with data : {}".format(
                        student_id,
                        student_email,
                        student_data))
        else:
            try:
                logging.info(
                    "Entering db for method add_student_to_subject with id : {} and email : {}".format(student_id,
                                                                                                       student_email))
                student_data = Student.objects.get(pk=student_id)
                logging.info(
                    "Exiting db for method add_student_to_subject with id : {} and email : {} with data : {}".format(
                        student_id, student_email,
                        student_data))
            except ObjectDoesNotExist:
                return Response({"status": "Failure",
                                 "message": "Unable to get student because student does not exist",
                                 "data": {}},
                                status=status.HTTP_404_NOT_FOUND)
        student = student_data.pk
        logging.info("Student id : {}".format(student))

        ## Get the subject details from the Subject Service
        ## For now keeping the subject id as 9999
        logging.info(
            "Entering Subject service for subject name : {} and subject id : {}".format(subject_name, subject_id))
        if subject_id is not None:
            subject = subject_id
        else:
            subject = random.randint(1, 1000)
        logging.info(
            "Exiting Subject service for subject name : {} and subject id : {} . Response subject details : {}".format(
                subject_name, subject_id, subject))
        logging.info("Subject id : {}".format(9999))

        ## Add the student subject data to table Student_Subjects
        serialized_data = StudentSubjectsSerializer(data={
            'student': student,
            'subject': subject
        })
        if serialized_data.is_valid():
            logging.info(
                "Entering db for method add_student_to_subject with student : {} and subject : {}".format(student,
                                                                                                          subject))
            serialized_data.save()

            logging.info(
                "Exiting db for method add_student_to_subject with student : {} and subject : {} . Response : {}".format(
                    student,
                    subject, serialized_data.data))
            return Response({"status": "Success",
                             "message": "Student and subject data added successfully",
                             "data": serialized_data.data},
                            status=status.HTTP_201_CREATED)
        else:
            logging.error("Serializer errors : {}".format(serialized_data.errors))
            return Response({"status": "Failure",
                             "message": "Serializer Errors",
                             "data": "{}".format(serialized_data.errors)},
                            status=status.HTTP_400_BAD_REQUEST)




    except Exception as e:
        logging.error("Some error occurred in method : add_student_to_subject. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def remove_subject_from_student(request):
    try:
        logging.info("Entering method remove_subject_from_student with request data : {}".format(request.data))
        student_id = request.GET.get('student_id')
        student_email = request.GET.get('student_email')
        subject_name = request.GET.get('subject_name')
        subject_id = request.GET.get('subject_id')

        ## Get the student details
        if student_id is None:
            if student_email is None:
                logging.error(
                    "student_id and student_email are both null for request {}. params : {}".format(request.data,
                                                                                                    request.GET))
                return Response({"status": "Failure",
                                 "message": "Unable to retrieve student data because student_id and student_email are both null",
                                 "data": {}},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                logging.info(
                    "Entering db for method remove_subject_from_student with id : {} and email : {}".format(student_id,
                                                                                                            student_email))
                student_data = Student.objects.get(email=student_email)
                logging.info(
                    "Exiting db for method remove_subject_from_student with id : {} and email : {} with data : {}".format(
                        student_id,
                        student_email,
                        student_data))
        else:
            try:
                logging.info(
                    "Entering db for method remove_subject_from_student with id : {} and email : {}".format(student_id,
                                                                                                            student_email))
                student_data = Student.objects.get(pk=student_id)
                logging.info(
                    "Exiting db for method remove_subject_from_student with id : {} and email : {} with data : {}".format(
                        student_id, student_email,
                        student_data))
            except ObjectDoesNotExist:
                return Response({"status": "Failure",
                                 "message": "Unable to get student because student does not exist",
                                 "data": {}},
                                status=status.HTTP_404_NOT_FOUND)
        student = student_data.pk
        logging.info("Student id : {}".format(student))

        ## Get the subject details from the Subject Service
        ## For now keeping the subject id as 9999
        logging.info(
            "Entering Subject service for subject name : {} and subject id : {}".format(subject_name, subject_id))
        if subject_id is not None:
            subject = subject_id
        else:
            subject = random.randint(1, 1000)
        logging.info(
            "Exiting Subject service for subject name : {} and subject id : {} . Response subject details : {}".format(
                subject_name, subject_id, subject))
        logging.info("Subject id : {}".format(9999))

        ## Remove the student subject data from table Student_Subjects
        try:
            logging.info(
                "Entering db for method remove_subject_from_student with id : {} and email : {}".format(student_id,
                                                                                                        student_email))
            student_subject_data = Student_Subjects.objects.get(student=student, subject=subject)
            student_subject_data.delete()
            logging.info(
                "Exiting db for method remove_subject_from_student with id : {} and email : {}".format(student_id,
                                                                                                       student_email))
            return Response({"status": "Success",
                             "message": "Student un enrolled from subject successfully",
                             "data": {}},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"status": "Failure",
                             "message": "Unable to delete student's subject because student is not enrolled to this subject",
                             "data": {}},
                            status=status.HTTP_404_NOT_FOUND)




    except Exception as e:
        logging.error("Some error occurred in method : remove_subject_from_student. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_subject_for_student(request):
    try:
        logging.info("Entering method get_subject_for_student with request params : {}".format(request.GET))
        student_id = request.GET.get('id')
        student_email = request.GET.get('email')
        ## Get the student details
        if student_id is None:
            if student_email is None:
                logging.error(
                    "student_id and student_email are both null for request {}. params : {}".format(request.data,
                                                                                                    request.GET))
                return Response({"status": "Failure",
                                 "message": "Unable to retrieve student data because student_id and student_email are both null",
                                 "data": {}},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                logging.info(
                    "Entering db for method get_subject_for_student with id : {} and email : {}".format(student_id,
                                                                                                            student_email))
                student_data = Student.objects.get(email=student_email)
                logging.info(
                    "Exiting db for method get_subject_for_student with id : {} and email : {} with data : {}".format(
                        student_id,
                        student_email,
                        student_data))
        else:
            try:
                logging.info(
                    "Entering db for method get_subject_for_student with id : {} and email : {}".format(student_id,
                                                                                                            student_email))
                student_data = Student.objects.get(pk=student_id)
                logging.info(
                    "Exiting db for method get_subject_for_student with id : {} and email : {} with data : {}".format(
                        student_id, student_email,
                        student_data))
            except ObjectDoesNotExist:
                return Response({"status": "Failure",
                                 "message": "Unable to get student because student does not exist",
                                 "data": {}},
                                status=status.HTTP_404_NOT_FOUND)
        student_id = student_data.pk
        logging.info("Student id : {}".format(student_id))

        ## Get all the subjects for the student
        response = []
        try:
            logging.info(
                "Entering db for student_subject_data for method get_subject_for_student with id : {} and email : {}".format(student_id,
                                                                                                    student_email))
            student_subject_data = Student_Subjects.objects.filter(student=student_id)
            logging.info(
                "Exiting db for student_subject_data for method get_subject_for_student with id : {} and email : {} . Data : {}".format(
                    student_id,
                    student_email, student_subject_data))
            for student_subject in student_subject_data:
                response_dict = {}
                logging.info(str(student_subject.student))
                student_details = StudentSerializer(student_subject.student)
                response_dict['student'] = student_details.data
                subject_id = student_subject.subject
                ## Get the subject details from the Subject Service
                logging.info("Entering Subject service for subject id : {}".format(subject_id))
                subject = {"subject_id": subject_id, "subject_data": {}}
                logging.info(
                    "Exiting Subject service for subject id : {} . Response subject details : {}".format(subject_id,
                                                                                                         subject))
                logging.info("Subject id : {}".format(subject_id))

                response_dict['subject_details'] = subject
                response.append(response_dict)

            return Response({"status": "Success",
                             "message": "Got details for all subjects for student",
                             "data": response},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logging.error("Some error occurred in method : get_subject_for_student. Exception : {} ".format(e))
            return Response({"status": "Failure",
                             "message": "Some error occurred while retrieving the data",
                             "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    except Exception as e:
        logging.error("Some error occurred in method : get_subject_for_student. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
