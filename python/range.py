import sys
class Range:
    'A class to describe a range of values (minimum and maximum).'

    def __init__(self,string,min=sys.float_info.max*-1.,max=sys.float_info.max):
        self.string = string
        try:
            (min_tmp, max_tmp) = string.split(":")
            self.min = float(min_tmp)
            self.max = float(max_tmp)
        except:
            self.min = float(min)
            self.max = float(max)

    def inside(self,test):
        return (test>self.min and test<self.max)
