from __future__ import print_function

import os
import sys
import logging
import constants

import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.auth.exceptions as gexcept


def ReadContent(filepath: str) -> str:
    pass

def HandleCredentials(dir_cred='credentials.json', dir_token='token.json') -> Credentials:

    if not os.path.isdir(os.path.split(dir_cred)[0]) and os.path.split(dir_cred)[0] != '':
        os.makedirs(os.path.split(dir_cred)[0])
    
    if not os.path.isdir(os.path.split(dir_token)[0]) and os.path.split(dir_token)[0] != '':
        os.makedirs(os.path.split(dir_token)[0])

    creds = None

    if os.path.exists(dir_token):
        creds = Credentials.from_authorized_user_file(dir_token, constants.SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                dir_cred, constants.SCOPES)
            creds = flow.run_local_server(port=0)
        with open(dir_token, 'w') as token:
            token.write(creds.to_json())
    
    return creds


def GenerateGmailMessage(
        recipient: str, sender: str, content: str, subject: str
        ) -> EmailMessage:
    
    message = EmailMessage()
    message.set_content(content)
    message['To'] = recipient
    message['From'] = sender
    message['Subject'] = subject

    return message


def GenerateGmailMessages(
        recipients: list[str], sender: str, content: str, subject: str
        ) -> list[EmailMessage]:
    
    messages = [GenerateGmailMessage(recipient=val, sender=sender, content=content, subject=subject) for val in recipients]

    return messages

def GenerateGmailMessageGroup(
        recipients: list[str], sender: str, content: str, subject: str
        ) -> EmailMessage:
    
    recipient_str = ''
    for val in recipients:
        recipient_str += val + ', '
    message = EmailMessage()
    message.set_content(content)
    message['To'] = recipient_str
    message['From'] = sender
    message['Subject'] = subject

    return message

def SendGmailMessage(service, message) -> bool:
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    create_message = {'raw': encoded_message}

    send_message = (service.users().messages().send(
        userId="me", body=create_message).execute()
    )

    logging.info("Message sent with ID {}".format(send_message["id"]))

def GenerateGmailService(credentials):
    try:
        return build('gmail', 'v1', credentials=credentials)
    except HttpError:
        logging.error("Error generating the mail service")
        sys.exit()

def main():
    pass

if __name__ == '__main__':
    main()