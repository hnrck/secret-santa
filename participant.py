"""
The participant module

A module used to define the participants, create a list of participant from a
CSV file and shuffling the secret santas.
"""
from csv import reader


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
