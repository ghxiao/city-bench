#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import optparse
import psycopg2
import shlex, subprocess

conn_osm_d = "host=localhost port=5432 dbname={0} user=postgres password=ps"

#tag_limit = 20

def main(argv):

		
	parser = optparse.OptionParser()
	parser.add_option('--db', action="store", dest="namedb", default="")
	parser.add_option('--limit', action="store", dest="taglimit", default=20)
	
	
	(options, args) = parser.parse_args()

	default_db = options.namedb
	#if options.namedb != "":
	tag_limit = int(options.taglimit)

	print "Dataset Statistics for " + default_db
	
	
	conn_gis_string =  conn_osm_d.format(default_db)
	
    # Connect to a PostGIS database and open a cursor to perform database operations
	conn_gis = psycopg2.connect(conn_gis_string)

    # Set DB parameter
	conn_gis.set_client_encoding('UTF8')
    #conn_gis.execute("SET search_path TO \"$user\",gis,owl;") 
	
	
	# Fields for POINTS
	fields_osm_1 = ["landuse", "waterway", "amenity", "place",  "leisure", "access",  "operator", "shop", "tourism", "public_transport", "sport",  "religion"]; # "natural" not working

	fields_osm_2 = ["highway", "landuse", "barrier", "surface", "operator", "waterway", "route", "service"]

	fields_osm_3 = ["highway", "railway",  "service", "boundary", "surface", "operator", "bridge", "junction",  "tunnel", "toll"]
	
	
	print ",Field, Tag1, Tag2, Tag3, Tag4, Tag5,..."
	
	print "TABLE POINTS:"
	
	cur1 = conn_gis.cursor()
	
	for field in fields_osm_1:
		
		sql = "SELECT {0} AS tag, COUNT({0}) AS size FROM planet_osm_point WHERE {0} IS NOT NULL AND osm_id > 0 GROUP BY {0} ORDER BY size DESC;".format(field)
		
		cur1.execute(sql) 
		printResults(cur1, field, tag_limit)
			
		
	print "TABLE POLYGONS:"

	for field in fields_osm_1:
		
		sql = "SELECT {0} AS tag, COUNT({0}) AS size FROM planet_osm_polygon WHERE {0} IS NOT NULL AND osm_id > 0 GROUP BY {0} ORDER BY size DESC;".format(field)
		
		cur1.execute(sql) 
		printResults(cur1, field, tag_limit)
		


	print "TABLE LINES:"

	for field in fields_osm_2:
		
		sql = "SELECT {0} AS tag, COUNT({0}) AS size FROM planet_osm_line WHERE {0} IS NOT NULL AND osm_id > 0 GROUP BY {0} ORDER BY size DESC;".format(field)
		
		cur1.execute(sql) 
		printResults(cur1, field, tag_limit)
		
	
	print "TABLE ROADS:"

	for field in fields_osm_3:
		
		sql = "SELECT {0} AS tag, COUNT({0}) AS size FROM planet_osm_roads WHERE {0} IS NOT NULL AND osm_id > 0 GROUP BY {0} ORDER BY size DESC;".format(field)
		
		cur1.execute(sql) 
		printResults(cur1, field, tag_limit)
		
		
	cur1.close()
	conn_gis.close()
	

	
def printResults(cur1, field, tag_limit): 
	
	outStr = ""
	count = 0
	
	for stats in cur1:
		tag = stats[0]
		size = stats[1]
		
		outStr = outStr + tag.title() + " (" + str(size) + "), "
		count=count+1
		
		if(count>tag_limit):
			break;
			
	#print "FIELD: " + field.title()
	#print outStr	
	print ", " + field.title() + ", " + outStr
	
	

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])	
