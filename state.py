"""
State class, implementing a data-type for states on the U.S. map.
Holds seed pixel for PIL flood_fill(), state name, data point, and fill color.
"""
class State:

    def __init__(self, state_abbrev = 'EX', state_full = 'Example', state_data = 100, state_pixel = (0,0), state_fill = (255,255,255)):
        """
        init func
        :param state_abbrev: The abbreviation of the state (2 letter)
        :param state_full: The full name of the state
        :param state_data: The data point attached to the state
        :param state_pixel: The seed pixel of the state (as a two-value tuple containing x,y coordinates on the U.S. map image)
        :param state_fill: The computed fill color for the state (as a 3-value tuple containing r,g,b values)
        """
        self.state_abbrev = state_abbrev
        self.state_full = state_full
        self.state_data = state_data
        self.state_pixel = state_pixel
        self.state_fill = state_fill

    # GET AND SET NAME
    def get_name(self):
        """
        gets abbreviation and full name attributes
        :return: 2-val tuple containing abbrev,full
        """
        return (self.state_abbrev, self.state_full)

    def set_name(self, abbrev, full):
        """
        sets the abbreviation and full name attributes
        :param abbrev: see state_abbrev @ __init__
        :param full: see state_full @ __init__
        :return: None
        """
        self.state_abbrev = abbrev
        self.state_full = full
        return None

    # GET AND SET SEED PIXEL
    def get_pixel(self):
        """
        gets the state's seed pixel tuple
        :return: seed pixel tuple
        """
        return self.state_pixel

    def set_pixel(self, x, y):
        """
        sets the state's seed pixel tuple
        :return: None
        """
        self.state_pixel = (x,y)
        return None

    # GET AND SET STATE DATA POINT
    def get_data(self):
        """
        gets the state's data point
        :return: state data point
        """
        return self.state_data

    def set_data(self, data):
        """
        sets state's data point
        :param data: data point, usually as an int or float
        :return: None
        """
        self.state_data = data
        return None

    # GET AND SET STATE FILL COLOR
    def get_fill(self):
        """
        gets the state's fill color tuple
        :return: fill color r,g,b tuple
        """
        return self.state_fill

    def set_fill(self, r, g, b):
        """
        sets the state's fill color tuple
        :param r: red component
        :param g: green component
        :param b: blue component
        :return: None
        """
        self.state_fill = (r,g,b)
        return None