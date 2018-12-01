"""
MAT 2170: Lab 7
Support functions for Lab 7

Submitted by:
"""

import turtle
import csv


def skipAmount(maximumValue):
    """
    Determines an appropriate skip amounts for a bar chart

    Args:
        maximumValue: the largest frequency which appears on a bar chart

    Returns:
        A "skip" amount for drawing equally spaced intermediate lines along
        the y axis.  If the maximum value appears is M, then this skip value
        is as follows:
            max value                 skip
            ------------------------------
                     M <= 10             1
                10 < M <= 50             5
                50 < M <= 100           10
               100 < M <= 500           50
               500 < M <= 1,000        100
             1,000 < M <= 5,000        500
             5,000 < M <= 10,000     1,000
            10,000 < M <= 100,000   10,000
    """
    bounds = [10, 50, 100, 500, 1000, 5000, 10000, 100000]
    for bound in bounds:
        if(maximumValue <= bound):
            skip = int(bound/10)
            break
    if(skip != ''):
        return skip
    else:
        return False

    
def makeMapping(filename):
    """
    Creates a mapping based on a file of ordered pairs.

    Args:
        filename: the name of a file with ordered pairs, in CSV format.

    Returns:
        A dictionary d with d[a] = b for every ordered pair a,b which appears
        in the specified file.
    """
    f = open(filename)
    csvfile = csv.reader(f)
    dict = {}
    for row in csvfile:
        dict[row[0]] = row[1]
    f.close()
    return dict


def displayMapping(d):
    """
    Display the contents of a dictionary.

    Args:
        d: a dictionary

    Returns:
        None
    """
    keys = list(d.keys())
    for key in keys:
        print(key, '=>', d[key])


def makeInverseMapping(m):
    """
    Create the inverse of a given map.

    Args:
        m: a dictionary

    Returns:
        A dictionary d which gives the inverse mapping.  More precisely,
        if there are p key values, k_1, k_2, ..., k_p, which map to v,
        then d[v] = [k_1, k_2, ..., k_p].
    """
    d = {}
    keys = list(m.keys())
    for key in keys:
        if m[key] not in d:
            d[m[key]] = [key]
        else:
            d[m[key]].append(key)
    return d


def offerMenuItems(choices):
    """
    Offer a menu of items and offer a choice to be selected

    Args:
        choices: a list of menu choices

    Returns:
        For valid input, the option number is returned.  If an incorrect
        response is given, the value None is returned.
    """
    print('Choose from the following items:')
    for x in range(len(choices)):
        print(str(x)+'. ','  ',choices[x])
    return int(input('Enter your choice #:'))

    
def state(s, stateDict):
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


def computeFrequencies(aList):
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


def drawLine(myTurtle, Px, Py, Qx, Qy, color):
    """
    Draws a line segment from one point to another

    Args:
        myTurtle: a turtle
        Px, Py: coordinates of one endpoint
        Qx, Qy: coordinates of the other endpoint

    Returns:
        None
    """

    # Draw a line segment from point (Px, Py) to point (Qx, Qy)
    init_color = myTurtle.pencolor()
    myTurtle.up()
    myTurtle.goto(Px, Py)
    myTurtle.down()
    myTurtle.pencolor(color)
    myTurtle.goto(Qx, Qy)
    myTurtle.up()
    myTurtle.pencolor(init_color)


def drawBar(myTurtle, LLx, LLy, URx, URy, color):
    """
    Draws a filled rectangle, in a specified color,
    given coordinates of the lower left and upper right
    points of a rectangle

    Args:
        myTurtle: a turtle
        LLx, LLy: coordinates of lower left corner of the bar
        URx, URy: coordinates of upper right corner of the bar
        color: desired fill color for this bar

    Returns:
        None
    """
    # save init color
    init_fill = myTurtle.pencolor()
    # set color and begin fill
    myTurtle.fillcolor(color)
    myTurtle.begin_fill()
    # goto lower left point
    myTurtle.up()
    myTurtle.goto(LLx, LLy)
    myTurtle.down()
    # goto upper left point
    myTurtle.goto(LLx, URy)
    # goto upper right point
    myTurtle.goto(URx, URy)
    # goto lower right point
    myTurtle.goto(URx, LLy)
    # back to lower left
    myTurtle.goto(LLx, LLy)
    # end fill and reset colors
    myTurtle.end_fill()
    myTurtle.fillcolor(init_fill)
    return None


def frequencyChart(aList):
    """
    Draw a histogram for a given data set

    Args:
        aList: a list of data values

    Returns:
        None
    """

    # Size of labels
    fontSize = 12

    # dictionary of data items and their frequencies
    countDict = computeFrequencies(aList)

    # Produce a sorted list of the unique data items
    itemList = list(countDict.keys())
    itemList.sort()

    # Number of histogram bars needed, one for each item
    numItems = len(itemList)

    # Create a list of frequencies and find the largest one
    countList = countDict.values()
    maxFrequency = max(countList)

    # Establish graphics window, create turtle and turn off animation
    window = turtle.Screen()
    chartT = turtle.Turtle()
    turtle.tracer(0)

    # Set up the window coordinate system, leaving a 10% margin on all sides
    window.setworldcoordinates(-0.1 * numItems, -0.1 * maxFrequency,
                               1.1 * numItems, maxFrequency * 1.1)

    # Ensure the chart does not include an image of the turtle
    chartT.hideturtle()

    # horizontal offset for each bar
    offset = 0.5

    # specify how close labels should be to histogram bars
    xLabelOffset = 0.05 * numItems  # for vertical axis labels
    yLabelOffset = 0.05 * maxFrequency  # for horizontal axis labels

    # Draw a horizontal axis
    drawLine(chartT, 0, 0, numItems, 0, "black")

    # Draw horizontal guides
    skip = skipAmount(maxFrequency)
    num_guides = int(maxFrequency/skip)
    for x in range(1,num_guides+1):
        # draw line
        drawLine(chartT, 0, skip*x, numItems, skip*x, "gray")
        # write label
        chartT.goto(-xLabelOffset, skip*x)
        chartT.write(str(skip*x), font=("Helvetica", fontSize))

    # Add labels for vertical min and max (the frequency range)
    chartT.goto(-xLabelOffset, 0)
    chartT.write("0", font=("Helvetica", fontSize))
    chartT.goto(-xLabelOffset, maxFrequency)
    chartT.write(str(maxFrequency), font=("Helvetica", fontSize))

    # For each item, draw a bar of appropriate height
    for index in range(len(itemList)):
        # Move turtle to the current index for that item's bar, and label it
        chartT.goto(index + offset, -yLabelOffset)
        chartT.write(str(itemList[index]), align="center",
                     font=("Helvetica", fontSize))

        # Determine the current item's frequency
        barHeight = countDict[itemList[index]]

        # Draw a bar of the appropriate height
        center_pos = index + offset
        drawBar(chartT, center_pos - 0.3, 0, center_pos + 0.3, barHeight, "gainsboro")
        drawLine(chartT, center_pos, 0, center_pos, barHeight, "black")

    turtle.update()
    chartT.hideturtle()

    # Keep graphics window open until user dismisses it
    window.exitonclick()


def mean(aList):
    """
    Compute the mean of a list of values

    Args:
        aList: a list of values

    Returns:
        The mean of the given values
    """

    if len(aList) == 0:
        return None
    return sum(aList) / len(aList)


def standardDev(aList):
    """
    Compute the standard deviation of a list of values

    Args:
        aList: a list of values (assumed two or more)

    Returns:
        The standard deviation of the given values
    """

    theMean = mean(aList)

    if len(aList) <= 1:
        return 0

    total = 0
    for item in aList:
        difference = item - theMean
        diffsq = difference ** 2
        total = total + diffsq

    return math.sqrt(total / (len(aList) - 1))

