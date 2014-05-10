#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import optparse
from math import * 

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
			
			if tempList[self.position] == "bank": tempList[self.position] = "Bank"
			elif tempList[self.position] == "pharmacy": tempList[self.position] = "Pharmacy"
			elif tempList[self.position] == "cinema": tempList[self.position] = "Cinema"
			elif tempList[self.position] == "theatre": tempList[self.position] = "Theatre"
			elif tempList[self.position] == "fast_food": tempList[self.position] = "FastFood"
			elif tempList[self.position] == "restaurant": tempList[self.position] = "Restaurant"
			elif tempList[self.position] == "post_office": tempList[self.position] = "PostOffice"
			elif tempList[self.position] == "cafe": tempList[self.position] = "Cafe"
			elif tempList[self.position] == "bar": tempList[self.position] = "Bar"
			elif tempList[self.position] == "atm": tempList[self.position] = "ATM"
			elif tempList[self.position] == "pub": tempList[self.position] = "Pub"
			elif tempList[self.position] == "fuel": tempList[self.position] = "Fuel"
			elif tempList[self.position] == "parking": tempList[self.position] = "Parking"
			else:
				tempList[self.position] = "Amenity"
				
			return tuple(tempList)

		if self.group == "shop":
			
			if tempList[self.position] == "supermarket": tempList[self.position] = "Supermarket"
			elif tempList[self.position] == "bakery": tempList[self.position] = "Bakery"
			elif tempList[self.position] == "hairdresser": tempList[self.position] = "Hairdresser"
			elif tempList[self.position] == "shoes": tempList[self.position] = "ShoeShop"
			elif tempList[self.position] == "chemist": tempList[self.position] = "Chemist"
			elif tempList[self.position] == "butcher": tempList[self.position] = "Butcher"
			elif tempList[self.position] == "clothes": tempList[self.position] = "Clothes"
			elif tempList[self.position] == "kiosk": tempList[self.position] = "Kiosk"
			elif tempList[self.position] == "bicycle": tempList[self.position] = "BicycleShop"
			elif tempList[self.position] == "florist": tempList[self.position] = "Florist"
			else:
				tempList[self.position] = "Shop"
				
			return tuple(tempList)
		
		if self.group == "highway":
			
			if tempList[self.position] == "residential": tempList[self.position] = "ResidentialRoute"
			elif tempList[self.position] == "primary": tempList[self.position] = "PrimaryRoute"
			elif tempList[self.position] == "secondary": tempList[self.position] = "SecondaryRoute"
			elif tempList[self.position] == "tertiary": tempList[self.position] = "TertiaryRoute"
				
			return tuple(tempList)

		if self.group == "bank_role":
			
			sn = tempList[self.position].lower() 
			obj_name = ""
			if sn.find("bank austria")  >= 0 or sn.find("erste bank") >= 0 or sn.find("raiffeisen") >= 0  or sn.find("bank of ireland") >= 0 or sn.find("allied irish bank") >= 0 or sn.find("norvik") >= 0 or sn.find("swedbank") >= 0 or sn.find("seb") >= 0 or sn.find("ubs") >= 0 or sn.find("credit suisse") >= 0: obj_name = "BankLargOp"
			elif sn.find("bawag")  >= 0 or sn.find("hypo") >= 0  or sn.find("volksbank") >= 0 or sn.find("ulster bank") >= 0 or sn.find("permanennt tsb") >= 0 or sn.find("nordea") >= 0 or sn.find("ge money") >= 0 or sn.find("kantonalbank") >= 0 or sn.find("valiant") >= 0 or sn.find("bekb") >= 0: obj_name = "BankMediumOp"
			else:
				obj_name = "BankSmallOp"
				
			tempList[self.position] = obj_name
			return tuple(tempList)

		
		if self.group == "restaurant_role":
			
			sn = tempList[self.position].lower() 
			obj_name = ""
			if sn.find("curry")  >= 0 or sn.find("tandoor") >= 0 or sn.find("indian") >= 0: obj_name = "IndianCuisine"
			elif (sn.find("gasthaus") >= 0) or (sn.find("stuben") >= 0) or (sn.find("gasthof") >= 0) or sn.find("bier") >= 0 or sn.find("wirt")  >= 0 or sn.find("keller")  >= 0 or sn.find("hof")  >= 0 or sn.find("hotel")  >= 0 or sn.find("zum ")  >= 0: obj_name = "GermanCuisine"
			elif sn.find("beisl")  >= 0 or sn.find("schnitzel")  >= 0 or sn.find("wien")  >= 0 or sn.find("heuriger")  >= 0 : obj_name = "AustrianCuisine"
			elif sn.find("bistro")  >= 0 or sn.find("brasserie") >= 0 or sn.find("chez ") >= 0 or sn.find("les ") >= 0: obj_name = "FrenchCuisine"
			elif sn.find("pizza")  >= 0 or sn.find("pizze") >= 0 : obj_name = "ItalianCuisine"
			elif sn.find("asia")  >= 0 or sn.find("wok")  >= 0  or sn.find("thai")  >= 0:  obj_name = "AsianCuisine"
			elif sn.find("china")  >= 0 or sn.find("chine")  >= 0 or sn.find("great wall")  >= 0 or sn.find("hong")  >= 0: obj_name = "ChineseCuisine"
			elif sn.find("sushi")  >= 0 or sn.find("tokyo")  >= 0: obj_name = "JapaneseCuisine"
			elif sn.find("steak")  >= 0 or sn.find("grill")  >= 0 : obj_name = "AmericanCuisine"
			elif sn.find("pub")  >= 0 or sn.find("fish")  >= 0  or sn.find("inn")  >= 0 or sn.find("river")  >= 0 : obj_name = "EnglishCuisine"
			elif sn.find("ristorante") >= 0 or sn.find("casa") >= 0 or sn.find("trattoria")  >= 0  or sn.find("osteria")  >= 0 or sn.find("trattoria")  >= 0  or sn.find("il ") >= 0 or sn.find("da ") >= 0 or sn.find("la ") >= 0: obj_name = "ItalianCuisine"
			
			if len(obj_name)==0:
				return None
			else:
				tempList[self.position] = obj_name
				return tuple(tempList)
			
		return None


	def close(self):
		a = 0


if __name__ == "__main__":
	import sys
	main(sys.argv[1:])
