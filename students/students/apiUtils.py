class ApiUtils:
    def __init__(self):
        self.localhost_subjects = 'http://127.0.0.1:8001/'
        self.subjects_base_url = 'subject-apis/'
        self.get_subject_url = '{}{}subject/get/'.format(self.localhost_subjects,self.subjects_base_url)
        self.update_subject_url = '{}{}subject/update/'.format(self.localhost_subjects,self.subjects_base_url)
