#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import optparse
import shlex, subprocess
import rdflib

result_sep = ", " #" - "

def main(argv):

		
	parser = optparse.OptionParser()
	parser.add_option('--dir', action="store", dest="directory", default="")
	parser.add_option('-d', action="store", dest="directory", default="")
	parser.add_option('--file', action="store", dest="file", default=20)
	parser.add_option('-f', action="store", dest="file", default=20)
	
	
	(options, args) = parser.parse_args()

	dir_name = options.directory
	file_name = options.file
	
	from os import walk

	files = []
		
	if len(dir_name) > 0:
	
		for (dirpath, dirnames, filenames) in walk(dir_name):
			
			files.extend(filenames)
			break
			
		print "ABox Statistics for " + dir_name
	
	else:
	
		if len(file_name) > 0:
			files.append(file_name)
			print "ABox Statistics for " + file_name
		
		
		
	if len(files) == 0:
		sys.exit("No input file or directory specified.")

		
	conceptAssertions = {}	
	objRoleAssertions = {}
	dataRoleAssertions = {}

	for file_name in files:
				
		# Only process OWL, RDF, TTL (XML,)
		if file_name.find('.owl') == -1 and file_name.find('.rdf') == -1 and file_name.find('.ttl') == -1: # and file_name.find("xml") == 0
			continue
			
			
		print "Processing: " + file_name
		
		g=rdflib.Graph()
		#g.load('http://dbpedia.org/resource/Semantic_Web')
		#g.load(file_name)
		
		file_pathname = dir_name + file_name
		
		try:
		
			fmt = rdflib.util.guess_format(file_pathname)
			g.parse(file_pathname, format=fmt) # "turtle"
		
		except Exception, e:
			
			try:
				# Fallback is turtle
				g.parse(file_pathname, format="turtle") # 
			except Exception, e:
				print e
				continue
			
		#for s,p,o in g:
		#	print s,p,o
		
		# S=individual, P:rdf:type, =concept
		qres1 = g.query( "SELECT DISTINCT ?a ?b WHERE { ?a rdf:type ?b . }")
	
		
		for row in qres1:
			
			individual = row[0].__str__()
			concept = row[1].__str__()
			
			if concept not in conceptAssertions:
				conceptAssertions[concept] = 0
	
			iCount = conceptAssertions[concept] + 1
			conceptAssertions[concept] = iCount
			
			
		qres2 = g.query( "SELECT DISTINCT ?a ?b ?c WHERE { ?a ?b ?c . ?b rdf:type owl:ObjectProperty . }")
		
		for row in qres2:
			
			#print row
			
			individual1 = row[0].__str__()
			oRole = row[1].__str__()
			individual2 = row[2].__str__()
			
			if oRole not in objRoleAssertions:
				objRoleAssertions[oRole] = 0
	
			iCount = objRoleAssertions[oRole] + 1
			objRoleAssertions[oRole] = iCount
			
			
		qres3 = g.query( "SELECT DISTINCT ?a ?b ?c WHERE { ?a ?b ?c . ?b rdf:type owl:DatatypeProperty . }")
		
		for row in qres3:
			
			#print row
			
			individual1 = row[0].__str__()
			oRole = row[1].__str__()
			#individual2 = row[2].__str__()
			
			if oRole not in dataRoleAssertions:
				dataRoleAssertions[oRole] = 0
	
			iCount = dataRoleAssertions[oRole] + 1
			dataRoleAssertions[oRole] = iCount
			

	print "Concept Assertions:"
	
	for val in sorted(conceptAssertions, key=conceptAssertions.get, reverse=True):
		#print val + "  (" + str(conceptAssertions[val]) + ")"
		print str(conceptAssertions[val]) + result_sep + val
		
	#for concept, iCount in conceptAssertions.iteritems():
		
		#print concept + "  (" + str(iCount) + ")"
		
		
	print "Object Role Assertions:"		

	for val in sorted(objRoleAssertions, key=objRoleAssertions.get, reverse=True):
		#print val + "  (" + str(conceptAssertions[val]) + ")"
		print str(objRoleAssertions[val]) + result_sep + val
		

	
	print "Data Role Assertions:"		
	
	for val in sorted(dataRoleAssertions, key=dataRoleAssertions.get, reverse=True):
		#print val + "  (" + str(conceptAssertions[val]) + ")"
		print str(dataRoleAssertions[val]) + result_sep + val

	
	
	
		
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])	
