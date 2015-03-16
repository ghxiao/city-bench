#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import optparse
from math import * 
from random import randrange

class CustomScriptTransformOSMRandom():

	group = ""
	position = 0

	def open(self, parameter):

		# Our input has two parameter: 
		# 1: What kind of mappping (e.g., amenity, shops, etc.)
		# 2: Where in the input tuple (tupleIn) is the value which should be mapped.
		#    This is needed because we usually have an input of the form, e.g., <id, name, tag>. Here we would set the position=3
		
		vals = parameter.split(' ')
		self.group = vals[0]
		self.position = int(vals[1]) - 1
		


	def map(self, tupleIn):
		
		# If no position, tuple, or group do nothing
		if self.position < 0 or len(self.group) == 0 or len(tupleIn) < self.position:
			return tupleIn
				
		tempList = list(tupleIn)

		if self.group == "bank_role":
			
			# Generate a random nr between 1-4
			ranr = randrange(1,4)
			
			# if it is 4 we ignore (by return None), so we just map (and generate) 75%
			# Rest is straight forward we return the concept BankLargOp if 1, etc.
			if ranr > 3:
				return None
			elif ranr == 1:
				return "BankLargeOp"
			elif ranr == 2:
				return "BankMediumOp"
			elif ranr == 3:
				return "BankSmallOp"
				
				
		if self.group == "busstop_hasroof":
			
			ranr = randrange(1,2)
			
			# 50% change if it has a roof or not then return a xsd:boolean 
			if ranr == 1:
				return "true"
			elif ranr == 2:
				return "false"
				
			
		return None


	def close(self):
		#a = 0


if __name__ == "__main__":
	import sys
	main(sys.argv[1:])
