#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import optparse
import shlex, subprocess, shutil
from math import * 
#-n=1 one stable model; -silent only results; -nofacts only EDB predicates
#dlvCall = "dlv -silent -nofacts -n=1 {0} {1}"

class CustomScriptReader():

	fileEDB = ""
	fileIDB = ""

	# We have two input parameter: 1. is the EDB file (facts); 2. is the IDB file (the logic program)
	def open(self, parameter):

		vals = parameter.split('" ')
		
		self.fileEDB = vals[0].replace('\"', '')
		self.fileIDB = vals[1].replace('\"', '')

		
	def read(self):
		
		#print dlvCall.format(self.fileEDB, self.fileIDB)
		
		#output = subprocess.call(dlvCall.format(self.fileEDB, self.fileIDB), shell=True)
		#if error != 0: print ("Error in executing dlv: " + str(sproc)) 
		
		temp_args = []
		temp_args.append("dlv")
		temp_args.append("-silent")
		temp_args.append("-nofacts")
		temp_args.append("-n=1")
		temp_args.append(self.fileEDB)
		temp_args.append(self.fileIDB)
		
		p = subprocess.Popen(temp_args, stdout=subprocess.PIPE)

		output = p.communicate()[0]
		
		# The results (is for now) a single anwer set of the form: {col(minnesota,green), col(wisconsin,red), ..., col(ohio,green)}
    	
		# First remove the brackets	
		answerSet =  output[1: len(output)-1]
		
		#print answerSet
		
		atoms_split = answerSet.split(", ") # Space is important
		
		for asplit in atoms_split:
			
			atom = asplit.strip()
			posOpenBracket = atom.find('(')
			posCloseBracket = atom.find(')')
			if posOpenBracket > -1 and posCloseBracket > -1:
				
				predicate =  atom[0: posOpenBracket]
				#yield predicate
				temp1 = atom[posOpenBracket+1:posCloseBracket]
				values = temp1.split(",")
				values.insert(0, predicate)
				tuple_sep = tuple(values)
				#print tuple_sep
				yield tuple_sep
				#yield predicate, values[0], values[1]
				
				
	#def close(self):
	#	# Clean up

def main(argv):

	# Test
	dataReader = CustomScriptReader()
	
	#temp_list = []
	#temp_list.append("test_edb.dlv")
	#temp_list.append("est_idb.dlv")
	
	dataReader.open("\"test_edb.dlv\" \"test_idb.dlv\"")
	for tupleIn in dataReader.read():	
		print tupleIn
		
	#dataReader.close()

if __name__ == "__main__":
	import sys
	main(sys.argv[1:])
