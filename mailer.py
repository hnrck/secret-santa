#!/usr/bin/env python2.7

"""
Mailer.

Most of these functions are not mine and comes from:
https://developers.google.com/gmail/api/v1/reference/users/messages/send
and
https://developers.google.com/gmail/api/v1/reference/users/messages/delete
"""

import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
from sys import stderr

SCOPES = 'https://mail.google.com'
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
    except errors.HttpError, error:
        print >> stderr, 'An error occurred: %s' % error


def get_credentials():
    """
    Retrieve the credentials.

    Return:
        credentials.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
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
    except errors.HttpError, error:
        print >> stderr, 'An error occurred: %s' % error


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

    message = MIMEText(message_text)
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receiver
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send(sender, receiver, subject, message_text):
    """ Main function. """
    message = create_message(sender, receiver, subject, message_text)
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    user_id = "me"
    send_message(service, user_id, message)
