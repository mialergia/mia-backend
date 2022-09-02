from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid', 'https://www.googleapis.com/auth/gmail.readonly']


def get_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])
        
        return service

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred 44: {error}')

def send_message(service, message):
    try:
        print(service)
        message = service.users().messages().send(userId="me",
                body=message).execute()

        print('Message Id: {}'.format(message['id']))

        return message
    except Exception as e:
        print('An error occurred pp: {}'.format(e))
        return None

def create_message_with_attachment(
    to,
    subject,
    message_text,
    ):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = 'alergiamia@gmail.com'
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    raw_message = \
        base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
    return {'raw': raw_message.decode('utf-8')}
 

def send_email_confirmation(to, url):
    txt= "Bienvenido a MIA! \n\nEstás recibiendo este correo electrónico porque se creó una cuenta con el mail {} \n\nPara confirmar que esto es correcto, clickea desde el celular en el siguiente link: \n {} \n\nGracias!"
    message = txt.format(to, url)
    subject = "[MIA] Por favor confirmar dirección de correo electrónico"
    service = get_service()
    msg = create_message_with_attachment(to ,subject ,message)
    send_message(service, msg)
    

if __name__ == '__main__':
    get_service()