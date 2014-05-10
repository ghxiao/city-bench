#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import optparse
from math import * 

gml_name = "gml:featurename"
rdf_type = "rdf:type"
geo_point = "geo:point"
geo_line = "geo:line"
geo_poly = "geo:polygon"

#prefix_osm_points = "110"

class CustomScriptReader():

    relation = ""
    role = ""
    input1 = ""
    input2 = ""

    def open(self, parameter):

        vals = parameter.split('" ')

        self.relation = vals[0].replace('\"', '')
        self.input1 = vals[1].replace('\"', '')
        #print self.relation


    def read(self):

        dictNodes = {}

        #for i in range(len(results1)-1):
        #print self.input1, self.input2
        
        for nline1 in self.extract_id_geo(self.input1):

            #nline1 = results1[i]
            temp1 = nline1.split('|')
            obj_id1 = temp1[0]
            obj_geo1 = temp1[1]

            #print "Current: ",  obj_id1, obj_geo1
            posID = obj_geo1.find("LINESTRING")
            if posID >= 0:
                tempGeo = obj_geo1[posID+11: len(obj_geo1)-1]
                #print "B1: ", tempGeo
                points = tempGeo.split(',')

                if self.relation == "nodes":
            
                    for i in range(len(points)):
                    	tempPoint = points[i]
                    	tempPointID = tempPoint.replace(' ', '_').replace('.', '_').replace('-', '') # Create a unique ID from the cooridnates
                    	tempPointGeo = "SRID=4326;POINT("  + tempPoint + ")"
                    	
                    	if not (tempPointID in dictNodes):
                    		dictNodes[tempPointID] = ''
                    		yield (tempPointID, obj_id1, tempPointGeo)            

                if self.relation == "edges":
                            
                    for i in range(len(points) - 1):
                    	tempPoint1 = points[i]
                    	tempPointID1 = tempPoint1.replace(' ', '_').replace('.', '_').replace('-', '')  # Create a unique ID from the cooridnates
                    	tempPoint2 = points[i+1]
                    	tempPointID2 = tempPoint2.replace(' ', '_').replace('.', '_').replace('-', '') 
                    	yield (tempPointID1, tempPointID2)

    #def close():


    def extract_id_geo(self, file_name):

        #results = []

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
