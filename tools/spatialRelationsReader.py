#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import optparse
from math import * 

from osgeo import ogr
from shapely import *
from shapely.geometry import *
from shapely.wkt import *
#from shapely.wkb import *

Buffer_Distance_Iso = 0.01 #  0.001
Buffer_Quadrant_Segments = 3

gml_name = "gml:featurename"
rdf_type = "rdf:type"
geo_point = "geo:point"
geo_line = "geo:line"
geo_poly = "geo:polygon"

class CustomScriptReader():

    relation = ""
    role = ""
    input1 = ""
    input2 = ""
    distance = Buffer_Distance_Iso

    def open(self, parameter):

        vals = parameter.split('" ')

        self.relation = vals[0].replace('\"', '')
        self.input1 = vals[1].replace('\"', '')
        
        if len(vals) > 2:
        	self.input2 = vals[2].replace('\"', '')

        if len(vals) > 3:
        	self.distance = float(vals[3].replace('\"', ''))


        if self.input2 is None or len(self.input2) == 0: self.input2 = self.input1

    def read(self):

        #results1 = extract_id_geo(input1)
        #results2 = extract_id_geo(input2)

        for nline1 in self.extract_id_geo(self.input1):
           
            temp1 = nline1.split('|')
            obj_id1 = temp1[0]
            obj_geo1 = temp1[1]

            print "Current: ",  obj_id1
            #geo1 = ogr.CreateGeometryFromWkt(obj_geo1) # res.wkt
            geo1 = loads(obj_geo1)                                 
            if geo1 is None: continue

            for nline2 in self.extract_id_geo(self.input2):
            #for j in range(len(results2)-1):
                
                #snline2 = results2[j]
                temp2 = nline2.split('|')
                obj_id2 = temp2[0]
                obj_geo2 = temp2[1]

                if obj_id1 == obj_id2: continue

                geo2 = loads(obj_geo2)            
                if geo2 is None: continue

                #print "Current 2: ", obj_id1, obj_id2

                # Heuristics to speed up, only consider objects which are in a radius of 100 km (for large objects take the upper left corner)
                lon1 = 0.0; lat1 = 0.0; lon2 = 0.0; lat2 = 0.0;
                (lat1, lon1, maxx1, maxy1) = geo1.bounds
                (lat2, lon2, maxx2, maxy2) = geo2.bounds

                # Everything which is more then 20km of eachother is ignored
                distance = self.haversine(lon1, lat1, lon2, lat2)
                if distance > 20:   
                	continue

                if self.relation == "contains":
                    #print geo1.bounds, geo2.bounds
                    if geo1.contains(geo2):
                        #print obj_id1, self.role, obj_id2
                        yield (obj_id1, obj_id2)
                elif self.relation == "within":
                    if geo1.within(geo2):
                        yield (obj_id1, obj_id2)
                elif self.relation == "crosses":
                    if geo1.crosses(geo2):
                        yield (obj_id1, obj_id2)
                elif self.relation == "disjoint":
                    if geo1.disjoint(geo2):
                        yield (obj_id1, obj_id2)
                elif self.relation == "equals":
                    if geo1.equals(geo2):
                        yield (obj_id1, obj_id2)
                elif self.relation == "intersects":
                    if geo1.intersects(geo2):
                        yield (obj_id1, obj_id2)
                elif self.relation == "touches":
                    if geo1.touches(geo2):
                        yield (obj_id1, obj_id2)
                elif self.relation == "next":
                    
                    temp_geo = geo1.buffer(self.distance) #  Buffer_Distance_Iso, Buffer_Quadrant_Segments)¶
                    if temp_geo.contains(geo2): # Need to change this
                        print distance
                        yield (obj_id1, obj_id2)

    #def close():


    def haversine(self, lon1, lat1, lon2, lat2):
        #
        #Calculate the great circle distance between two points 
        #on the earth (specified in decimal degrees)
        #
        
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        return km



    def extract_id_geo(self, file_name):

        with open(file_name, 'r') as f1:

            actID = actGeo = ""
            lines = f1.readlines()
             
            for i in range(len(lines)-1):
                nline = lines[i]

                posID = nline.find(rdf_type)
                if posID > 0: # tuwi:24820994 rdf:type tuwt:Playground, owl:NamedIndividual;
                    actID = nline[0:posID-1]

                posGeo = -1
                posGeo = nline.find(geo_point)
                if posGeo == -1:
                    posGeo = nline.find(geo_line)
                    if posGeo == -1:
                        posGeo = nline.find(geo_poly)
                        if posGeo == -1:
                            posGeo = nline.find(geo_line)
                if posGeo >= 0: #  geo:polygon "0103000020E610000"
                    posGeo2 = nline.find('\"')
                    posGeo3 = nline.find('^')

                    actGeo = nline[posGeo2+1: posGeo3-1]
                    temp3 = actGeo.split(';') # Remove SRID=4326;
                    #results.append(actID + '|' + temp3[1])
                    if len(temp3) > 1:
                        yield actID + '|' + temp3[1]



            f1.closed

        #return results



if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
