#!/usr/bin/env python2.7


"""
Main file.

Take a list of partipants in a CSV file, create the secret santa couples, and
send messages.
"""


from sys import argv, stderr
from participant import participants_parser
from participant import participants_shuffler
from participant import participants_mail


def help_message():
    """ Help message. """
    print >> stderr, ""
    print >> stderr, argv[0], "<participant_file>.csv"
    print >> stderr, ""
    print >> stderr, "\twhere participant file contains lines like this:"
    print >> stderr, "\t\t<firstname> <name>, <mail@mail.mail>."
    print >> stderr, ""


def main():
    """ Main function. """
    if len(argv) <= 1:
        raise AssertionError(
            'Error: A CSV file containing participants is needed.')

    if len(argv) > 2:
        raise AssertionError('Error: A single CSV file is needed.')

    csv_file = argv[1]
    if csv_file[-4:] != ".csv":
        raise AssertionError('Error: The argument might not be a csv file.')

    participants = participants_parser(csv_file)
    couples = participants_shuffler(participants)
    participants_mail(couples)

if __name__ == '__main__':
    try:
        main()
    except AssertionError, err:
        print >> stderr, str(err)
        help_message()
