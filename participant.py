"""
The participant module

A module used to define the participants, create a list of participant from a
CSV file and shuffling the secret santas.
"""
from csv import reader
from random import shuffle
from mailer import send


class Participant(object):
    """
    The Participant class

    holds and shows information about secret santa participant.

    Args:
        name: The name of the participant.
        mail: The mail of the participant (with potentially unncessary spaces).
    """

    def __init__(self, name, mail):
        """ The participant constructor. Take a name and a mail as argument,
        and return a participant. """
        self.__name = name
        self.__mail = mail.replace(' ', '')

    def __get_name(self):
        """ Name getter. """
        return self.__name

    def __get_mail(self):
        """ Mail getter. """
        return self.__mail

    name = property(__get_name, None, None,
                    'The participant name, set at creation, not modificable.')

    mail = property(__get_mail, None, None,
                    'The participant mail, set at creation, not modificable.')

    def __str__(self):
        """ Shows participant info when casted to string. """
        return self.__name + ' (' + self.__mail + ')'

    def mail_santa(self, target):
        """ Send to the secret santa its target. """
        if not isinstance(target, Participant):
            raise TypeError('Error: Target is not a participant.')
        send('', self.mail, f'Hello {self.name}! This is your secret target!',
             f"Hi {self.name}!\n\nYou are {target.name}'s secret santa!\n\nGood luck! Have Fun!")


def participants_parser(csv_file):
    """
    Participants parser.

    Args:
        csv_file: a CSV file containing the participants name and their mails.

    Return:
        A list of Participant

    Raises:
        AssertionError: Argument is null
        IOError: missing file.
        TypeError: Argument is not a string
        ValueError: illformated values in file.
    """
    if csv_file is None:
        raise AssertionError('Error: nothing to parse.')

    if not isinstance(csv_file, str):
        raise TypeError('Error: csv_file is not a string.')

    participants = []

    with open(csv_file) as csv_lines:
        csv_rows = reader(csv_lines)

        for row in csv_rows:
            if len(row) != 2:
                raise ValueError('Error: illformated csv file.')
            participants.append(Participant(row[0], row[1]))

    return participants


def participants_shuffler(participants):
    """
    Participants shuffler.

    Args:
    participants: The list of participants.

    Return:
        A list couple of participant, where the first one is the secret santa
        of the second one.

    Raises:
        AssertionError: Missing argument, or to few participants.
        TypeError: The argument is no a list of participants.
    """
    if participants is None:
        raise AssertionError('Error: No participants to shuffle :-(')

    if not isinstance(participants, list):
        raise TypeError('Error: participants arg in participant_shuffler must'
                        ' be a list of Participant.')

    for participant in participants:
        if not isinstance(participant, Participant):
            raise TypeError(
                'Error:', str(participant), ' is not a Participants.')

    if len(participants) == 1:
        raise AssertionError('It\'s not fun to play alone :-(')

    shuffle(participants)
    couples = list(zip(participants, participants[1:] + [participants[0]]))

    return couples


def participants_mail(couples):
    """
    Mail all the secret Santas.

    Args:
        couples: The couples secret santa / target.
    """
    for participant, target in couples:
        print(f"Sending {participant.name} target")
        participant.mail_santa(target)
