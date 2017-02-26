# Region Verifier // GeoFilter
# DESCRIPTION
# The purpose of this module is to provide more advanced location based
# filtering which is not properly provided by the filtering system of the Streaming API.
# This was part of the original Twitter Downloader, but may not have been made in a modular manner.
# INPUT
# Bounding Box
# tweet location
# decision parameters
# OUTPUT
# true/false
# ADDITIONAL RESOURCES
# https://dev.twitter.com/streaming/overview/request-parameters
# 1? example of input object? --assume first, find example later
# 2? boundary values for Rochester region box? --find from the code ricky uploaded
# 3? class/function? --class
# 4? other criteria for a given region to be 'True'? overlap ratio?

class GeoFilter(object):
    '''
    a filter class, where a target region is given as input for GeoFilter()
    then, a function called CheckRegion could return T/F and ratio of a
    certain point/region is within or without the target region and by
    how much
    '''
    def __init__(self, target_region=[-78.5401367286, 42.00027541, -76.18272114, 43.3301514]):
        #target region shall be given in [x_min, y_min, x_max, y_max]
        self.tar = target_region
        if len(self.tar) != 4:
            raise ValueError

    def CheckRegion(self,geoinfo,overlap=0.8):
        # return T if the point/region is within the target region, False else
        # first, if it's a point, we check whether it lies within the target region
        if len(geoinfo) == 2:
            R_type = "Point"
            x = float(geoinfo[0])
            y = float(geoinfo[1])
        elif len(geoinfo) == 4:
            R_type = "Region"
            x_min = float(geoinfo[0])
            y_min = geoinfo[1]
            x_max = geoinfo[2]
            y_max = geoinfo[3]

        tar_x_min = float(self.tar[0])
        tar_y_min = float(self.tar[1])
        tar_x_max = float(self.tar[2])
        tar_y_max = float(self.tar[3])
        Decision = False
        if R_type == "Point":
            if x >= tar_x_min and x <= tar_x_max and y >= tar_y_min and y <= tar_y_max:
                Decision = True
                ratio = 1
                print "input point lies inside the target region \n"
        elif R_type == "Region":
            if x_min >= tar_x_min and x_max <= tar_x_max and y_min >= tar_y_min and y_max <= tar_y_max:
                Decision = True
                ratio = 1
                print "input region lies inside the target region completely \n"
            elif x_min > tar_x_max or x_max < tar_x_min or y_min > tar_y_max or y_max < tar_y_min:
                print "input region lies outside the target region completely \n"
                ratio = 0
            else:
                print "ratio calculation"
                if x_max > tar_x_max:
                    width = abs(tar_x_max - x_min)
                else:
                    width = abs(x_max - tar_x_min)
                #print "width = %f" %width
                #print type(width)
                if y_min > tar_y_min:
                    height = abs(y_min - tar_y_max)
                else:
                    height = abs(tar_y_min - y_max)
                #print "height = %f" % height
                #print type(height)
                overlap_area = width * height
                #print type(overlap_area)
                area = abs(y_max - y_min) * abs(x_max - x_min)
                #print "area = %f" %area
                #print type(area)
                ratio = round(overlap_area/area,3)
                #print type(ratio)
                #print "input region lies inside the target region partially:"
                print "%f percent of the input region lies inside the target region \n" % ratio
                if ratio >= overlap:
                    Decision = True
        return Decision, ratio


####test#####
Rochester = GeoFilter()
Rectangular = GeoFilter([0,0,100,100])
overlap = 0.8
#test1 = Rochester.CheckRegion([-77, 43],overlap)
#passed

#test2 = Rectangular.CheckRegion([50,50])
#passed

#test3 = Rectangular.CheckRegion([10,10,20,20])
#passed

test4 = Rectangular.CheckRegion([50,50,150,150])
#passed


