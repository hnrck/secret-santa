#!/usr/bin/env python3

"""
Simple test module to test the participant shuffler.
"""

from participant import Participant, participants_parser, participants_shuffler


def null_arg():
    """ Null argument. """
    try:
        _ = participants_shuffler(None)
    except AssertionError:
        print('Exception catched. Great')
        return 1, 1
    else:
        print('Error: Exception not catched')
        return 0, 1


def bad_type_arg():
    """ Argument is an int not a list. """
    try:
        _ = participants_shuffler(0)
    except TypeError:
        print('Exception catched. Great')
        return 1, 1
    else:
        print('Error: Exception not catched')
        return 0, 1


def bad_type_list():
    """ The list is a list of int, not participants. """
    try:
        _ = participants_shuffler(list(range(10)))
    except TypeError:
        print('Exception catched. Great')
        return 1, 1
    else:
        print('Error: Exception not catched')
        return 0, 1


def solo():
    """ Only one participant, its too few. """
    try:
        _ = participants_shuffler([Participant("", "")])
    except AssertionError:
        print('Exception catched. Great')
        return 1, 1
    else:
        print('Error: Exception not catched')
        return 0, 1


def good():
    """ Good test, should work. """
    try:
        participants = participants_parser("test.csv")
        couples = participants_shuffler(participants)
        for couple in couples:
            print(str(couple[0]), '->', str(couple[1]))
        print("File Parsed. Great.")
        return 1, 1
    except:
        return 0, 1


def main():
    """ Main function of parse test. """
    tests = [null_arg, bad_type_arg, bad_type_list, solo, good]
    nb_valid, nb_test = 0, 0
    for test in tests:
        print("Test: ", str(test), test.__doc__)
        tmp_nb_valid, tmp_nb_test = test()
        nb_valid += tmp_nb_valid
        nb_test += tmp_nb_test
    print("Tests: " + str(nb_valid) + "/" + str(nb_test))


if __name__ == '__main__':
    main()
