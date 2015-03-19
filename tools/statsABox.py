#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import optparse
import shlex, subprocess
import rdflib

def main(argv):

		
	parser = optparse.OptionParser()
	parser.add_option('--dir', action="store", dest="directory", default="")
	parser.add_option('--file', action="store", dest="file", default=20)
	
	
	(options, args) = parser.parse_args()

	dir_name = options.directory
	file_name = options.file
	
	print "ABox Statistics for " + file_name
	

	g=rdflib.Graph()
	#g.load('http://dbpedia.org/resource/Semantic_Web')
	#g.load(file_name)
	
	g.parse(file_name, format="turtle")
	
	#for s,p,o in g:
	#	print s,p,o
	
	# S=individual, P:rdf:type, =concept
	qres = g.query( "SELECT DISTINCT ?a ?b WHERE { ?a rdf:type ?b . }")

	conceptAssertions = {}
	
	for row in qres:
		
		individual = row[0].__str__()
		concept = row[1].__str__()
		
		if concept not in conceptAssertions:
			conceptAssertions[concept] = 0

		iCount = conceptAssertions[concept] + 1
		conceptAssertions[concept] = iCount
		
	
	for val in sorted(conceptAssertions, key=conceptAssertions.get, reverse=True):
		#print val + "  (" + str(conceptAssertions[val]) + ")"
		print str(conceptAssertions[val]) + " - " + val
		
		
	#for concept, iCount in sortedConcepts:
		
	#for concept, iCount in conceptAssertions.iteritems():
		
		#print concept + "  (" + str(iCount) + ")"
		
	

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])	
