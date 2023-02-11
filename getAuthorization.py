import requests_oauthlib
import webbrowser
import json
import os
import easygui
import requests
from api_handler import BrightspaceAPI

from appFuncs import getConfig as getConfig
from appFuncs import saveConfig as saveConfig
from appFuncs import authorize as authorize
from appFuncs import parseAuthCode as parseAuthCode
from appFuncs import accessToken as accessToken

tokenConfigFile = 'tokenConfig'

conf = getConfig(tokenConfigFile)

if 'access_token' in conf and 'refresh_token' in conf:
    print('Access token and refresh token already available.')
else:
    auth = authorize(tokenConfigFile)
    webbrowser.open_new_tab(auth)
    print('Authorizing...')
    print('Please enter the URL from the browser:')
    enterAuthCode = input()

    ac = parseAuthCode(enterAuthCode)
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
include_whoami = easygui.ynbox(
    'Would you like to include a WHOAMI GET call in the application?')
if include_whoami:
    headers = {'Authorization': 'Bearer ' + conf['access_token']}
    r = requests.get(
        'https://fieldx.brightspace.com/d2l/api/whoami', headers=headers)
    if r.status_code == 200:
        print(r.json())
    else:
        print('WHOAMI GET call failed with status code:', r.status_code)


access_token = conf["access_token"]
api_url = "https://davidm.brightspacedemo.com"

api = BrightspaceAPI(access_token, api_url)

print("What would you like to do?")
print("1. Get Courses")
print("2. Get Enrollments")
print("3. Get Course Details")
print("4. Get User Details")
print("5. Create Discussion Topic")
print("6. Get Org Units")
print("7. Check Course Completion")
print("8. Get Org Name")
print("9. Find Org with Students")
print("10. Get User ID")
print("11. Get Org Structure")
print("12. Get User ID from Username")

choice = 1

while choice != 0:

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

        