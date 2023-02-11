#sean Baker
# 2023-02-11

import requests
import json

class BrightspaceAPI:
    def __init__(self, access_token, api_url):
        self.access_token = access_token
        self.api_url = api_url
        self.headers = {
            'Authorization': 'Bearer ' + self.access_token,
             'Content-Type': 'application/json',
             'Accept': 'application/json'
            
        }
        self.org_structure = {}
        self.org_tree = []
        self.org_courses = []

    def get_courses(self):
        url = self.api_url + '/d2l/api/lp/1.0/courses/'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_enrollments(self, course_id):
        url = self.api_url + '/d2l/api/lp/1.0/enrollments/' + str(course_id)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_course_details(self, course_id):
        url = self.api_url + '/d2l/api/lp/1.0/courses/' + str(course_id)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_user_details(self, user_id):
        url = self.api_url + '/d2l/api/lp/1.0/users/' + str(user_id)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_discussion_topic(self, course_id, title, message):
        url = self.api_url + '/d2l/api/lp/1.0/discussions/' + str(course_id)
        payload = {
            "Title": title,
            "Message": message
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return response.json()
    def get_org_structure(self):
        response = requests.get(f'{self.api_url}/d2l/api/lp/1.10/orgstructure/', headers=self.headers)
        return json.loads(response.text)


    def get_org_units(self, org_unit_id=6606):
        url = self.api_url + '/d2l/api/lp/1.20/orgstructure/{}'.format(org_unit_id) + '/children/'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        org_units = response.json()
        return org_units

    def check_course_completion(self, org_unit_id):
        url = self.api_url + '/d2l/api/lp/1.0/enrollments/orgUnits/' + str(org_unit_id) + '/users/'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        enrollments = response.json()
        for enrollment in enrollments['Items']:
            if enrollment['IsCourseCompleted'] == True:
                return True
        return False

    def get_org_name(self, org_unit_id):
        url = self.api_url + '/d2l/api/lp/1.0/orgstructure/' + str(org_unit_id)
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        org_unit = response.json()
        return org_unit['Name']

    def find_org_with_students(self):
        url = self.api_url + '/d2l/api/lp/1.0/orgstructure/'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        org_units = response.json()
        for org_unit in org_units['Identifier'] == 'CourseOffering':
            print(org_unit) 
            if org_unit['Identifier'] == 'CourseOffering':
                url = self.api_url + '/d2l/api/lp/1.0/enrollments/orgUnits/' + str(org_unit['Identifier']) + '/users/'
                response = requests.get(url, headers=headers)
                enrollments = response.json()
                for enrollment in enrollments['Items']:
                    if enrollment['User']['Identifier'] == self.get_user_id() and enrollment['User']['Profile']['Email'].endswith('@mycollege.edu'):
                        return self.get_org_name(org_unit['ParentOrganizationUnitId'])
        return None

    def get_user_id(self):
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Accept': 'application/json'
        }
        url = self.api_url + '/d2l/api/lp/1.0/users/whoami'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['Identifier']
        else:
            return None
    def get_user_id_from_username(self, username):
        url = self.api_url + '/d2l/api/lp/1.0/users/'
        params = {'userName': username}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            users = response.json()
            return users[0]['UserId']
        return None
    
    def unenroll_student_from_class(self, username, class_id):
        url = self.api_url + '/d2l/api/lp/1.0/enrollments/classes/' + str(class_id) + '/users/' + str(self.get_user_id_from_username(username))
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            return True
        return False

    def get_enrolled_courses(self, username):
        user_id = self.get_user_id_from_username(username)
        url = self.api_url + '/d2l/api/lp/1.0/enrollments/users/' + str(user_id) + '/orgs/'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            courses = response.json()
            return courses
        return None

    def enroll_student_in_class(self, username, class_id):
        user_id = self.get_user_id_from_username(username)
        url = self.api_url + '/d2l/api/lp/1.0/enrollments/classes/' + str(class_id) + '/users/' + str(user_id)
        data = {
            'IsActive': True,
            'RoleId': 1
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            return True
        return False
    

    def get_org_tree(self, org_units=6606):
        orgs_data = self.get_org_units(org_units)
       
        if len(orgs_data) != 0:
            for org in orgs_data:
                if org['Identifier'] not in self.org_structure:
                    self.org_structure[org['Identifier']] = {
                        "Name": org["Name"],
                        "Type": {"code": org["Type"]["Code"], "name": org["Type"]["Name"]},
                        "parentOrgUnitId": org["parentOrgUnitId"],
                        "children": [],
                        "courses": []
                    }
                if org['parentOrgUnitId'] != None:
                    parent = self.org_structure.get(org["parentOrgUnitId"], {})
                    parent.setdefault("children", []).append(org['Identifier'])

                if "Course" not in org["Type"]["Code"]:
                    self.org_tree.append(org["Identifier"])
                else:
                    courses = self.get_courses(org["Identifier"])
                    self.org_structure[org['Identifier']]['courses'].extend(courses)
                   
        for org_id in self.org_tree:
            self.get_org_tree(org_id, self.org_structure, self.org_courses)

        return self.org_structure


        

    def get_courses(self, org_id=6606):

        courses_response = requests.get(f'{self.api_url}/d2l/api/lp/1.0/courses/?orgUnitId={org_id}', headers=self.headers)
        courses_data = courses_response.json()
        for course in courses_data['Items']:
            course_id = course['Identifier']
            course_name = course['Name']
            self.org_structure[org_id]['courses'].append({'id': course_id, 'name': course_name})

        return self.org_structure[org_id]

    def get_user_id_from_username(self, username):
        url = self.api_url + '/d2l/api/lp/1.0/users/'
        params = {'userName': username}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            users = response.json()
        return users['UserId']