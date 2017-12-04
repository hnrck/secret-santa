"""
The participant module

A module used to define the participants, create a list of participant from a
CSV file and shuffling the secret santas.
"""


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
