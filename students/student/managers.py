import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from students.logging import logging
from students.apiUtils import ApiUtils

globals()['api_utils'] = ApiUtils()

class StudentManager:

    @staticmethod
    def get_subject(subject_name,subject_id):
        try:
            logging.info("Entering method get_subject for id : {} , name : {}".format(subject_id,subject_name))
            try:
                logging.info("Calling API to get subject details -- get_subject_url")
                response = requests.get(api_utils.get_subject_url,params={'id':subject_id,'name':subject_name})
                logging.info("Response from API to get subject details -- get_subject_url : {}".format(response.json()))
                return (response,'found')
            except Exception as e:
                logging.error("Some error occurred while getting data"
                              "from subjects service : {} ".format(e))
                raise Exception(e)

        except Exception as e:
            logging.error("Some error occurred in method : get_subject_by_id. Exception : {} ".format(e))
            raise Exception(e)




