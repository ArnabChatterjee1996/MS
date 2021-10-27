import random

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from subjects.logging import logging
from .managers import SubjectManager
from .serializers import *
from .models import Subject


@api_view(['GET'])
def server_health(request):
    return Response({"health_status": "OK"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.atomic
def add_subject(request):
    try:
        logging.info("Entering method add_subject with request data : {}".format(request.data))
        serialized_data = SubjectSerializer(data=request.data)
        if serialized_data.is_valid():
            logging.info(
                "Starting db transaction for method add_subject . Data : {}".format(serialized_data.validated_data))
            serialized_data.save()
            logging.info("Exiting db transaction for method add_subject. Data : {}".format(serialized_data.data))
            return Response({"status": "Success",
                             "message": "Subject added Successfully",
                             "data": "{}".format(serialized_data.data)},
                            status=status.HTTP_201_CREATED)

        else:
            logging.error("Serializer errors : {}".format(serialized_data.errors))
            return Response({"status": "Failure",
                             "message": "Serializer Errors",
                             "data": "{}".format(serialized_data.errors)},
                            status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error("Some error occurred in method : add_subject. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_subject(request):
    try:
        logging.info("Entering method get_subject")
        id = request.GET.get('id')
        name = request.GET.get('name')
        if id is None:
            if name is None:
                logging.error("id and name are both null for request . Params : {}".format(request.GET))
                return Response({"status": "Failure",
                                 "message": "Unable to retrieve data because id and name are both null",
                                 "data": {}},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    logging.info("Entering Manager class for name : {}".format(name))
                    subject_details = SubjectManager.get_subject_by_name(name=name)
                    if subject_details[1] == 'found':
                        subject = subject_details[0]
                        serialized_data = SubjectSerializer(subject)
                        return Response({"status": "Success",
                                         "message": "Subject data retrieved successfully",
                                         "data": serialized_data.data},
                                        status=status.HTTP_200_OK)
                    elif subject_details[1] == 'not_found':
                        return Response({"status": "Failure",
                                         "message": "There is no subject with this name",
                                         "data": {}},
                                        status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    logging.error("Some error occurred in method : get_subject. Exception : {} ".format(e))
                    return Response({"status": "Failure",
                                     "message": "Some error occurred while retrieving the data",
                                     "data": "Some exception occurred while getting the data . Exception : {}".format(
                                         e)},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                logging.info("Entering Manager class for name : {}".format(name))
                subject_details = SubjectManager.get_subject_by_id(id=id)
                if subject_details[1] == 'found':
                    subject = subject_details[0]
                    serialized_data = SubjectSerializer(subject)
                    return Response({"status": "Success",
                                     "message": "Subject data retrieved successfully",
                                     "data": serialized_data.data},
                                    status=status.HTTP_200_OK)
                elif subject_details[1] == 'not_found':
                    return Response({"status": "Failure",
                                     "message": "There is no subject with this name",
                                     "data": {}},
                                    status=status.HTTP_404_NOT_FOUND)



            except Exception as e:

                logging.error("Some error occurred in method : get_subject. Exception : {} ".format(e))

                return Response({"status": "Failure",

                                 "message": "Some error occurred while retrieving the data",

                                 "data": "Some exception occurred while getting the data . Exception : {}".format(

                                     e)},

                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logging.error("Some error occurred in method : get_subject. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@transaction.atomic
def get_all_subjects(request):
    try:
        logging.info("Entering method get_all_subjects")
        subjects = SubjectManager.get_all_subjects()
        serialized_data = SubjectSerializer(subjects[0],many=True)
        return Response({"status": "Success",
                         "message": "Subjects data retrieved successfully",
                         "data": serialized_data.data},
                        status=status.HTTP_200_OK)
    except Exception as e:
        logging.error("Some error occurred in method : get_all_subjects. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@transaction.atomic
def update_subject(request):
    try:
        logging.info("Entering method update_subject")
        id = request.GET.get('id')
        name = request.GET.get('name')
        try:
            add_student = request.GET.get('add_student')
            logging.info("add_student param is available for request : {}".format(request.GET))
        except:
            logging.error("add_student param is not available for request : {}".format(request.GET))
            add_student = None
        if id is None:
            if name is None:
                logging.error("id and name are both null for request . Params : {}".format(request.GET))
                return Response({"status": "Failure",
                                 "message": "Unable to retrieve data because id and name are both null",
                                 "data": {}},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    logging.info("Entering Manager class for name : {}".format(name))
                    subject_details = SubjectManager.get_subject_by_name(name=name)
                    if subject_details[1] == 'found':
                        subject = subject_details[0]
                        serialized_data = SubjectSerializer(subject, data=request.data,partial=True)
                        if serialized_data.is_valid():
                            serialized_data.save()
                            if subject_details[1] == 'found':
                                if add_student is not None:
                                    if add_student == 'inc':
                                        logging.info(
                                            "Increasing students_opted count by 1 for subject : {}".format(
                                                subject_details))
                                        subject = subject_details[0]
                                        logging.info("Starting db transaction for method update_subject")
                                        subject.students_opted += 1
                                        subject.save()
                                        logging.info(
                                            "Exiting db transaction for method update_subject . Data : {}".format(
                                                subject))
                                    elif add_student == 'dec':
                                        logging.info(
                                            "Increasing students_opted count by 1 for subject : {}".format(
                                                subject_details))
                                        subject = subject_details[0]
                                        logging.info("Starting db transaction for method update_subject")
                                        if subject.students_opted > 0 :
                                            subject.students_opted -= 1
                                            subject.save()
                                        else:
                                            logging.error("Not decreasing students_opted because students_opted is 0")
                                        logging.info(
                                            "Exiting db transaction for method update_subject . Data : {}".format(
                                                subject))
                                    else:
                                        logging.info("Not changing students_opted count for subject : {} . "
                                                     "add_student value : {}".format(subject_details, add_student))
                            return Response({"status": "Success",
                                             "message": "Subject data updated successfully",
                                             "data": serialized_data.data},
                                            status=status.HTTP_200_OK)
                        else:
                            logging.error("Serializer errors : {}".format(serialized_data.errors))
                            return Response({"status": "Failure",
                                             "message": "Serializer Errors",
                                             "data": "{}".format(serialized_data.errors)},
                                            status=status.HTTP_400_BAD_REQUEST)
                    elif subject_details[1] == 'not_found':
                        return Response({"status": "Failure",
                                         "message": "There is no subject with this name",
                                         "data": {}},
                                        status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    logging.error("Some error occurred in method : get_subject. Exception : {} ".format(e))
                    return Response({"status": "Failure",
                                     "message": "Some error occurred while retrieving the data",
                                     "data": "Some exception occurred while getting the data . Exception : {}".format(
                                         e)},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                logging.info("Entering Manager class for id : {}".format(id))
                subject_details = SubjectManager.get_subject_by_id(id=id)
                if subject_details[1] == 'found':
                    subject = subject_details[0]
                    serialized_data = SubjectSerializer(subject,data=request.data,partial=True)
                    if serialized_data.is_valid():
                        serialized_data.save()
                        if subject_details[1] == 'found':
                            if add_student is not None:
                                if add_student == 'inc':
                                    logging.info(
                                        "Increasing students_opted count by 1 for subject : {}".format(subject_details))
                                    subject = subject_details[0]
                                    logging.info("Starting db transaction for method update_subject")
                                    subject.students_opted += 1
                                    subject.save()
                                    logging.info(
                                        "Exiting db transaction for method update_subject . Data : {}".format(subject))
                                elif add_student == 'dec':
                                    logging.info(
                                        "Increasing students_opted count by 1 for subject : {}".format(subject_details))
                                    subject = subject_details[0]
                                    logging.info("Starting db transaction for method update_subject")
                                    if subject.students_opted > 0:
                                        subject.students_opted -= 1
                                        subject.save()
                                    else:
                                        logging.error("Not decreasing students_opted because students_opted is 0")
                                    logging.info(
                                        "Exiting db transaction for method update_subject . Data : {}".format(
                                            subject))
                                    logging.info(
                                        "Exiting db transaction for method update_subject . Data : {}".format(subject))
                                else:
                                    logging.info("Not changing students_opted count for subject : {} . "
                                                 "add_student value : {}".format(subject_details, add_student))
                        return Response({"status": "Success",
                                         "message": "Subject data updated successfully",
                                         "data": serialized_data.data},
                                        status=status.HTTP_200_OK)
                    else:
                        logging.error("Serializer errors : {}".format(serialized_data.errors))
                        return Response({"status": "Failure",
                                         "message": "Serializer Errors",
                                         "data": "{}".format(serialized_data.errors)},
                                        status=status.HTTP_400_BAD_REQUEST)
                elif subject_details[1] == 'not_found':
                    return Response({"status": "Failure",
                                     "message": "There is no subject with this name",
                                     "data": {}},
                                    status=status.HTTP_404_NOT_FOUND)
            except Exception as e:

                logging.error("Some error occurred in method : update_subject. Exception : {} ".format(e))

                return Response({"status": "Failure",

                                 "message": "Some error occurred while retrieving the data",

                                 "data": "Some exception occurred while getting the data . Exception : {}".format(

                                     e)},

                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    except Exception as e:
        logging.error("Some error occurred in method : update_subject. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@transaction.atomic
def delete_subject(request):
    try:
        logging.info("Entering method delete_subject")
        id = request.GET.get('id')
        name = request.GET.get('name')
        if id is None:
            if name is None:
                logging.error("id and name are both null for request . Params : {}".format(request.GET))
                return Response({"status": "Failure",
                                 "message": "Unable to retrieve data because id and name are both null",
                                 "data": {}},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    logging.info("Entering Manager class for name : {}".format(name))
                    subject_details = SubjectManager.get_subject_by_name(name=name)
                    if subject_details[1] == 'found':
                        subject = subject_details[0]
                        subject.delete()
                        return Response({"status": "Success",
                                             "message": "Subject data deleted successfully",
                                             "data": {}},
                                            status=status.HTTP_200_OK)
                    elif subject_details[1] == 'not_found':
                        return Response({"status": "Failure",
                                         "message": "There is no subject with this name",
                                         "data": {}},
                                        status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    logging.error("Some error occurred in method : delete_subject. Exception : {} ".format(e))
                    return Response({"status": "Failure",
                                     "message": "Some error occurred while retrieving the data",
                                     "data": "Some exception occurred while getting the data . Exception : {}".format(
                                         e)},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                logging.info("Entering Manager class for id : {}".format(id))
                subject_details = SubjectManager.get_subject_by_id(id=id)
                if subject_details[1] == 'found':
                    subject = subject_details[0]
                    subject.delete()
                    return Response({"status": "Success",
                                         "message": "Subject data deleted successfully",
                                         "data": {}},
                                        status=status.HTTP_200_OK)
                elif subject_details[1] == 'not_found':
                    return Response({"status": "Failure",
                                     "message": "There is no subject with this name",
                                     "data": {}},
                                    status=status.HTTP_404_NOT_FOUND)
            except Exception as e:

                logging.error("Some error occurred in method : delete_subject. Exception : {} ".format(e))

                return Response({"status": "Failure",

                                 "message": "Some error occurred while retrieving the data",

                                 "data": "Some exception occurred while getting the data . Exception : {}".format(

                                     e)},

                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logging.error("Some error occurred in method : delete_subject. Exception : {} ".format(e))
        return Response({"status": "Failure",
                         "message": "Some error occurred while retrieving the data",
                         "data": "Some exception occurred while getting the data . Exception : {}".format(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
