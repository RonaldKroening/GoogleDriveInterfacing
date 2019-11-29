from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile
from oauth2client.client import GoogleCredentials
import requests
import re
import http
from pydrive import *
import sys
import os
from apiclient import errors
# 1. Authenticate and create the PyDrive client.

gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)
ids = []
filechecknum = []
#Replace with names of files to upload
files = ['personalinfo.txt','UserInputClassification.py',"updating.py",'notes.txt', "reminder.txt", "alarms.txt", "termsandrefs.txt", 'phraseandresp.txt', 'people.txt', 'todolist.txt', 'usedwebsites.txt', 'preferredwebsites.txt']
filestocheckfordeleting = ['personalinfo.txt', 'UserInputClassification.txt', "updating.txt",
    'notes.txt', "reminder.txt", "alarms.txt", "termsandrefs.txt",
    'phraseandresp.txt', 'people.txt', 'todolist.txt', 'usedwebsites.txt',
    'preferredwebsites.txt'
]
#To update, files must be deleted first to be replaced.
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()


def upload_file():
    for f in files:
        if f == 'UserInputClassification.py':
            #Python Files cannot be uploaded to Google Drive via the API, thus they are converted to .txt before uploaded.
            #Formatting stays the same despite the conversion
            os.getcwd()
            print(os.getcwd())
            os.rename("UserInputClassification.py", "UserInputClassification.txt")
            file1 = drive.CreateFile({'title': f})
            g = open(f, 'r')
            contents = g.read()
            file1.SetContentFile(str(contents))
            file1.Upload()
        elif f == 'updating.py':
            os.getcwd()
            print(os.getcwd())
            os.rename("updating.py", "updating.txt")
            file1 = drive.CreateFile({'title': f})
            g = open(f, 'r')
            contents = g.read()
            file1.SetContentFile(str(contents))
            file1.Upload()
        else:
            file1 = drive.CreateFile({'title': f})
            g = open(f, 'r')
            contents = g.read()
            file1.SetContentFile(str(contents))
            file1.Upload()
def download_file():
    for file1 in file_list:
        if file1['title'] in files:
            if file1['title'] == 'UserInputClassification.txt':
                file_obj = drive.CreateFile({'id': file1['id']})
                file_obj.GetContentFile(file1, mimetype='txt')
                os.getcwd()
                os.rename("UserInputClassification.txt", "UserInputClassification.py")
            elif file1['title'] == 'updating.txt':
                file_obj = drive.CreateFile({'id': file1['id']})
                file_obj.GetContentFile(file1, mimetype='txt')
                os.getcwd()
                os.rename("updating.txt", "updating.py")

            else:
                file_obj = drive.CreateFile({'id': file1['id']})
                file_obj.GetContentFile(file1, mimetype='txt')

# ...
file = drive.CreateFile()


def delete_files_in_drive():
    for file1 in file_list:
        filechecknum.append(0)
        filechecknum.append(file1['title'])
        file = drive.CreateFile({'id' : file1['id']})
        if file1['title'] in filestocheckfordeleting:
            #if title in drive is one of the project's files
            pos = filechecknum.index(file1['title'])
            valpos = pos - 1
            #valpos is the number of times file is seen
            filechecknum[valpos] += 1
            for d in filechecknum:
                if d.isInstance(d, int):
                    #differentiate between file name and appearences
                    if d > 1:
                        #if file in more than once
                        file.Delete()
def delete_files_on_device():
    filechecknum = []
    for f in files:
        os.getcwd()
        if os.path.exists(f):
            pos = filechecknum.index(f)
            valpos = pos - 1
            #valpos is the number of times file is seen
            filechecknum[valpos] += 1
            for d in filechecknum:
                if d.isInstance(d, int):
                    #differentiate between file name and appearences
                    if d > 1:
                        os.remove(f)

