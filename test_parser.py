#!/usr/bin/env python2.7

"""
Simple test module to test the participant parser.
"""

from participant import participants_parser


def null_arg():
    """ Null argument. """
    try:
        _ = participants_parser(None)
    except AssertionError:
        print 'Exception catched. Great'
        return 1, 1
    else:
        print 'Error: Exception not catched'
        return 0, 1


def bad_type_arg():
    """ Argument is an int not a str. """
    try:
        _ = participants_parser(0)
    except TypeError:
        print 'Exception catched. Great'
        return 1, 1
    else:
        print 'Error: Exception not catched'
        return 0, 1


def no_file():
    """ No file on disk. """
    try:
        _ = participants_parser("something_that_does_not_exist")
    except IOError:
        print 'Exception catched. Great'
        return 1, 1
    else:
        print 'Error: Exception not catched'
        return 0, 1


def illformated_file():
    """ Illformated file. """
    try:
        _ = participants_parser("illformated_test.csv")
    except ValueError:
        print 'Exception catched. Great'
        return 1, 1
    else:
        print 'Error: Exception not catched'
        return 0, 1


def good():
    """ Good test, should work. """
    try:
        participants = participants_parser("test.csv")
        for participant in participants:
            print str(participant)
        print "File Parsed. Great."
        return 1, 1
    except:
        print "Something happened."
        return 0, 1


def main():
    """ Main function of parse test. """
    tests = [null_arg, bad_type_arg, no_file, illformated_file, good]
    nb_valid, nb_test = 0, 0
    for test in tests:
        print "Test: ", str(test), test.__doc__
        tmp_nb_valid, tmp_nb_test = test()
        nb_valid += tmp_nb_valid
        nb_test += tmp_nb_test
    print "Tests: " + str(nb_valid) + "/" + str(nb_test)

if __name__ == '__main__':
    main()
