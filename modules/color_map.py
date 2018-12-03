class ColorMap:

    def __init__(self, min_color, max_color, min_val, max_val):
        self.min_c = min_color # 3-val r,g,b tuple
        self.max_c = max_color # 3-val r,g,b tuple
        self.min_v = min_val
        self.max_v = max_val

    def compute_color(self, data_point):
        """
        Computes and returns the 3-val rgb tuple for the given data point
        :param data_point: a number between min_val and max_val
        :return: the 3-val r,g,b tuple
        """
        # get range
        range = self.max_v - self.min_v
        # get data ratio to overall range
        data_dist = data_point - self.min_v
        data_percent = data_dist/range
        # compute red
        r_range = self.max_c[0] - self.min_c[0]
        r_add = data_percent*r_range
        R = self.min_c[0] + r_add
        # compute green
        g_range = self.max_c[1] - self.min_c[1]
        g_add = data_percent * g_range
        G = self.min_c[1] + g_add
        # compute blue
        b_range = self.max_c[2] - self.min_c[2]
        b_add = data_percent * b_range
        B = self.min_c[2] + b_add
        # RETURN
        return (round(R),round(G),round(B))