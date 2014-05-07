#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import optparse
from math import * 
import psycopg2

Buffer_Distance_Iso = 0.01 # 100m

class CustomScriptReader():

    conn_gis = None
    cur_gis = None

    relation = ""
    connection = ""
    table1 = ""
    table1Cond = ""
    table2 = ""
    table2Cond = ""
    distance = Buffer_Distance_Iso

    def open(self, parameter):

        vals = parameter.split('" ')

        self.connection = vals[0].replace('\"', '')

        self.relation = vals[1].replace('\"', '')
        
        print self.connection
        
        self.table1 = vals[2].replace('\"', '')
        self.table2 = vals[3].replace('\"', '')

        self.table1Cond = vals[4].replace('\"', '')
        self.table2Cond = vals[5].replace('\"', '')

        if len(vals) > 6:
            self.table1GeomColumn = vals[6].replace('\"', '')
        else:
            self.table1GeomColumn = 'way'

        if len(vals) > 7:
            self.table2GeomColumn = vals[7].replace('\"', '')
        else:
            self.table2GeomColumn = 'way'

        if len(vals) > 8:
            self.table1IdColumn =  vals[8].replace('\"', '')
        else:
            self.table2IdColumn = 'osm_id'

        if len(vals) > 9:
            self.table2IdColumn =  vals[9].replace('\"', '')
        else:
            self.table2IdColumn = 'osm_id'

        if len(vals) > 10:
            self.distance = float(vals[10].replace('\"', ''))
            

         # Connect to a PostGIS database and open a cursor to perform database operations
        self.conn_gis = psycopg2.connect(self.connection)
        # Set DB parameter
        self.conn_gis.set_client_encoding('UTF8')
        self.cur_gis = self.conn_gis.cursor()
        

    def read(self):
 
        spatialRelation = ""
 
        if self.relation == "contains":
            spatialRelation = "ST_Contains(t1.{0}, t2.{1})".format(self.table1GeomColumn, self.table2GeomColumn)

        elif self.relation == "within":
            spatialRelation = "ST_Within(t1.{0}, t2.{1})".format(self.table1GeomColumn, self.table2GeomColumn)

        elif self.relation == "crosses":
            spatialRelation = "ST_Crosses(t1.{0}, t2.{1})".format(self.table1GeomColumn, self.table2GeomColumn)
            
        elif self.relation == "disjoint":
            spatialRelation = "ST_Disjoint(t1.{0}, t2.{1})".format(self.table1GeomColumn, self.table2GeomColumn)
            
        elif self.relation == "equals":
            spatialRelation = "ST_Equals(t1.{0}, t2.{1})".format(self.table1GeomColumn, self.table2GeomColumn)
            
        elif self.relation == "intersects":
             spatialRelation = "ST_Intersects(t1.{0}, t2.{1})".format(self.table1GeomColumn, self.table2GeomColumn)
             
        elif self.relation == "touches":
             spatialRelation = "ST_Touches(t1.{0}, t2.{1})".format(self.table1GeomColumn, self.table2GeomColumn)

        elif self.relation == "next":   
             spatialRelation = "ST_Distance(t1.{0}, t2.{1}) < {2}".format(self.table1GeomColumn, self.table2GeomColumn, self.distance)
       
    
        # sourceQueryTemplate = "SELECT t1.osm_id, t2.osm_id FROM planet_osm_point as t1 INNER JOIN planet_osm_polygon AS t2 ON ST_Contains(t2.way, t1.way) WHERE t1.amenity IS NOT NULL AND  t2.landuse IS NOT NULL AND t1.osm_id > 0 and  t2.osm_id > 0"
        sourceQueryTemplate = "SELECT t1.{0}, t2.{1} FROM {2} as t1 INNER JOIN {3} AS t2 ON {4} WHERE {5} AND {6} AND t1.{0} > 0 and t2.{1} > 0"
        sourceQuery = sourceQueryTemplate.format(self.table1IdColumn, self.table2IdColumn, self.table1, self.table2, spatialRelation, self.table1Cond, self.table2Cond) 
          
        print sourceQuery
          
        # Run query
        self.cur_gis.execute(sourceQuery)
        
        for tuple_gis in self.cur_gis:

             yield tuple_gis   
             #yield (obj_id1, obj_id2)
    
    

    def close(self):

        self.cur_gis.close()
        self.conn_gis.close()




if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
