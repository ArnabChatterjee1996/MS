from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from subjects.logging import logging
from .models import Subject

class SubjectManager:

    @staticmethod
    @transaction.atomic
    def get_subject_by_id(id):
        try:
            logging.info("Entering method get_subject_by_id for id : {}".format(id))
            try:
                logging.info("Starting db transaction for method get_subject_by_id . id : {}".
                             format(id))
                subject = Subject.objects.get(pk=id)
                logging.info("Exiting db transaction for method get_subject_by_id. Data . id : {}".
                             format(id))
                return (subject,'found')
            except ObjectDoesNotExist:
                return (None,'not_found')

        except Exception as e:
            logging.error("Some error occurred in method : get_subject_by_id. Exception : {} ".format(e))
            raise Exception(e)

    @staticmethod
    @transaction.atomic
    def get_subject_by_name(name):
        try:
            logging.info("Entering method get_subject_by_name for id : {}".format(name))
            try:
                logging.info("Starting db transaction for method get_subject_by_name . id : {}".
                             format(name))
                subject = Subject.objects.get(name=name)
                logging.info("Exiting db transaction for method get_subject_by_name. Data . id : {}".
                             format(name))
                return (subject, 'found')
            except ObjectDoesNotExist:
                return (None, 'not_found')

        except Exception as e:
            logging.error("Some error occurred in method : get_subject_by_name. Exception : {} ".format(e))
            raise Exception(e)

    @staticmethod
    @transaction.atomic
    def get_all_subjects():
        try:
            logging.info("Entering method get_all_subjects")
            logging.info("Starting db transaction for method get_all_subjects")
            subjects = Subject.objects.all()
            logging.info("Exiting db transaction for method get_all_subjects")
            return (subjects, 'found')

        except Exception as e:
            logging.error("Some error occurred in method : get_all_subjects. Exception : {} ".format(e))
            raise Exception(e)


