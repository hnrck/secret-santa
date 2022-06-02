"""
Mailer.

Most of these functions are not mine and come from:
https://developers.google.com/gmail/api/v1/reference/users/messages/send
and
https://developers.google.com/gmail/api/v1/reference/users/messages/delete
"""
import base64

import httplib2
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
from apiclient import errors, discovery
from sys import stderr

SCOPES = ['https://mail.google.com/']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Send Email'


def delete_message(service, user_id, msg_id):
    """Delete a Message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      msg_id: ID of Message to delete.
    """
    try:
        service.users().messages().delete(userId=user_id, id=msg_id).execute()
    except errors.HttpError as error:
        print('An error occurred: %s' % error, file=stderr)


def get_credentials():
    """
    Retrieve the credentials.

    Return:
        credentials.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            home_dir = os.path.expanduser('~')
            credential_dir = os.path.join(home_dir, '.credentials')
            credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
            flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    return credentials


def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
                 can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (
            service.users().messages().send(
                userId=user_id, body=message).execute()
        )
        delete_message(service, user_id, message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error, file=stderr)


def create_message(sender, receiver, subject, message_text):
    """
    Create a message for an email.

    Args:
        sender: Email address of the sender.
        receiver: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """

    message: MIMEText = MIMEText(message_text)
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receiver
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send(sender, receiver, subject, message_text):
    """ Main function. """
    message = create_message(sender, receiver, subject, message_text)
    credentials = get_credentials()
    service = discovery.build('gmail', 'v1', credentials=credentials)
    user_id = "me"
    send_message(service, user_id, message)
