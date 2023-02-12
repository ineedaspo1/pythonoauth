# Sean Baker 
# 2023-02-11
#Brightspace API Functions

import requests_oauthlib
import webbrowser
import json
import os
import easygui
import requests
from api_handler import BrightspaceAPI
import time 
from appFuncs import getConfig as getConfig
from appFuncs import saveConfig as saveConfig
from appFuncs import authorize as authorize
from appFuncs import parseAuthCode as parseAuthCode
from appFuncs import accessToken as accessToken

tokenConfigFile = 'tokenConfig'

conf = getConfig(tokenConfigFile)

if conf['access_token'] != '':
    auth = authorize(tokenConfigFile)
    webbrowser.open_new_tab(auth)
    print('Authorizing...')
    

    
    AuthCode = input("please enter code:")


    ac = parseAuthCode(AuthCode)
    conf['auth_code'] = ac[0]
    conf['state'] = ac[1]

    accToken = accessToken(conf)
    conf['access_token'] = accToken['access_token']
    conf['refresh_token'] = accToken['refresh_token']
    conf['expires_at'] = accToken['expires_at']
    saveConfig(tokenConfigFile, conf)
    print('Access token and refresh token saved.')

    print('Access token:', conf['access_token'])
    print('Refresh token:', conf['refresh_token'])



access_token = conf["access_token"]
print(access_token)
api_url = "https://davidm.brightspacedemo.com"

api = BrightspaceAPI(access_token, api_url)

print("What would you like to do?")
print("1. Get List of Courses")
print("2. Get User Enrollments")
print("3. View Course Details")
print("4. View User Profile Information")
print("5. Create a New Discussion Topic")
print("6. Get Organization Units")
print("7. Check a User's Course Completion Status")
print("8. Get the Name of an Organization")
print("9. Find Organizations with Enrolled Students")
print("10. Get a User's ID")
print("11. View the Structure of an Organization")
print("12. Get User ID from User's Email Address")
print("13. Unenroll a Student from a Class")
print("14. Get a User's Enrolled Courses")
print("15. Create a New Student")


choice = 0
while choice <= 20:
    choice = int(input("Enter the number of your choice: "))
    if choice == 1:
        courses = api.get_courses()
        print(courses)
    elif choice == 2:
        course_id = int(input("Enter the course ID: "))
        enrollments = api.get_enrollments(course_id)
        print(enrollments)
    elif choice == 3:
        course_id = int(input("Enter the course ID: "))
        course_details = api.get_course_details(course_id)
        print(course_details)
    elif choice == 4:
        user_id = int(input("Enter the user ID: "))
        user_details = api.get_user_details(user_id)
        print(user_details)
    elif choice == 5:
        course_id = int(input("Enter the course ID: "))
        title = input("Enter the title: ")
        message = input("Enter the message: ")
        response = api.create_discussion_topic(course_id, title, message)
        print(response)
    elif choice == 6:
        org_units = api.get_org_units()
        print(org_units)
    elif choice == 7:
        org_unit_id = int(input("Enter the org unit ID: "))
        completion = api.check_course_completion(org_unit_id)
        print(completion)
    elif choice == 8:
        org_unit_id = int(input("Enter the org unit ID: "))
        org_name = api.get_org_name(org_unit_id)
        print(org_name)
    elif choice == 9:
        org_with_students = api.find_org_with_students()
        print(org_with_students)
    elif choice == 10:
        user_id = api.get_user_id()
        print(user_id)
    elif choice == 11:
        org_structure = api.get_org_structure()
        print(org_structure)
    elif choice == 12:
        username = input("Enter the username: ")
        user_id = api.get_user_id_from_username(username)
        print(user_id)
    elif choice == 13:
        user_id = int(input("Enter the user ID: "))
        org_unit_id = int(input("Enter the org unit ID: "))
        unenroll_user = api.unenroll_student_from_class(org_unit_id, user_id)
        print(unenroll_user)
    elif choice == 14:
        username = input("Enter the user name: ")
        enrolled_courses = api.get_enrolled_courses(username=username)
        print(enrolled_courses)
    elif choice == 15:
        first_name = input("Enter the first name: ")
        last_name = input("Enter the last name: ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        email = input("Enter the email: ")
        create_student = api.create_student(first_name, last_name, username, password, email)
        print(create_student)
    elif choice == 16:
        course_id = int(input("Enter the course ID: "))
        enrollments = api.get_enrollments(course_id)
        print(enrollments)
    elif choice == 17:
        course_id = int(input("Enter the course ID: "))
        user_id = int(input("Enter the user ID: "))
        user_progress = api.get_user_progress(course_id, user_id)
        print(user_progress)
    elif choice == 18:
        course_id = int(input("Enter the course ID: "))
        user_id = int(input("Enter the user ID: "))
        user_grade = api.get_user_grades(course_id, user_id)
        print(user_grade)




