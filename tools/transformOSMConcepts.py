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


class CustomScriptTransform():

	group = ""
	position = 0

	def open(self, parameter):

		vals = parameter.split(' ')
		self.group = vals[0]
		self.position = int(vals[1]) - 1

	def map(self, tupleIn):
		
		# If no position, tuple, or group do nothing
		if self.position == 0 or len(self.group) == 0 or len(tupleIn) < self.position:
			return tupleIn
		
		tempList = list(tupleIn)

		if self.group == "amenity":
			
			if tempList[self.position] == "bank": tempList[self.position] = "tuwt:Bank"
			elif tempList[self.position] == "pharmacy": tempList[self.position] = "tuwt:Pharmacy"
			elif tempList[self.position] == "cinema": tempList[self.position] = "tuwt:Cinema"
			elif tempList[self.position] == "theatre": tempList[self.position] = "tuwt:Theatre"
			elif tempList[self.position] == "fast_food": tempList[self.position] = "tuwt:FastFood"
			elif tempList[self.position] == "restaurant": tempList[self.position] = "tuwt:Restaurant"
			elif tempList[self.position] == "post_office": tempList[self.position] = "tuwt:PostOffice"
			elif tempList[self.position] == "cafe": tempList[self.position] = "tuwt:Cafe"
		
		if self.group == "highway":
			
			if tempList[self.position] == "residential": tempList[self.position] = "tuwt:ResidentialRoute"
			elif tempList[self.position] == "primary": tempList[self.position] = "tuwt:PrimaryRoute"
			elif tempList[self.position] == "secondary": tempList[self.position] = "tuwt:SecondaryRoute"
			elif tempList[self.position] == "tertiary": tempList[self.position] = "tuwt:TertiaryRoute"
				
			return tuple(tempList)
		
		return None


	def close(self):
		a = 0


if __name__ == "__main__":
	import sys
	main(sys.argv[1:])
