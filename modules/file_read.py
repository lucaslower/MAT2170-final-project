"""
file read module
reads in csv data file, converts to dict {'state_abbrev':data_point}
"""

import csv, importlib.util
# import state_class
spec = importlib.util.spec_from_file_location('state_class', '/var/www/projects.lucaslower.com/us-map/modules/state.py')
state_class = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state_class)


def parse_state(s, stateDict):
    """
    Find a 2-letter state abbreviation within space-separated string s

    Args:
        s: a string
        stateDict: a dictionary with the states as keys

    Returns:
        If the string has a two-letter state abbreviation (e.g., IL)
        somewhere within it, then it returns this state;
        otherwise it returns None.
    """
    s_split = s.split()
    for state_abrev in stateDict:
        if state_abrev in s_split:
            return state_abrev


def compute_frequencies(aList):
    """
    Compute a frequency distribution of a given data set

    Args:
        aList: a list of data values

    Returns:
        A dictionary consisting of (item, frequency) pairs
    """

    # dictionary of data items and their frequencies
    countDict = {}

    # determine how many times each data item appears in the list
    for item in aList:
        if item in countDict:
            # item has been seen before; boost its count
            countDict[item] = countDict[item] + 1
        else:
            # first time this item has been seen
            countDict[item] = 1

    return countDict


def read_csv_file_frequency(filename,state_col,state_dict):
    """
    reads a file and converts it to a dictionary
    :param filename: the .csv file to process
    :param state_col: the column in which the state abbreviation appears
    :param state_dict: the dictionary containing all state abbreviations to check for
    :return: dictionary {'state_abbrev':frequency}
    """
    csvfile = open(filename, encoding='utf-8')
    csvreader = csv.reader(csvfile)
    freq_states = []
    for row in csvreader:
        if row[0][0] != '#':
            state_abrev = parse_state(row[state_col],state_dict)
            freq_states.append(state_abrev)
    csvfile.close()
    return compute_frequencies(freq_states)


def read_csv_file_raw(filename):
    """
    reads a file and converts it to a dictionary
    :param filename: the .csv file to process
    :return: dictionary {'state_abbrev':data_point}
    """
    d = {}
    csvfile = open(filename, encoding='utf-8')
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0][0] != '#':
            d[row[0]] = float(row[1])
    csvfile.close()
    return d


def read_pixel_file():
    """
    reads the state_pixels file
    :return: list of State() classes
    """
    state_d = {}
    f = open("/var/www/projects.lucaslower.com/us-map/data_files/state_pixels.csv", 'r')
    csvf = csv.reader(f)
    for row in csvf:
        if row[0][0] != '#':
            state = state_class.State(row[0], 0, (int(row[1]),int(row[2])), 0)
            state_d[row[0]] = state
    f.close()
    return state_d
