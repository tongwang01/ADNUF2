#This is the main program pulling inventory on funda
import requests
import time
import sys
from get_property_list import get_property_list
from get_features import get_features

def get_inventory(backfill = False):
	inventory = []
	properties = get_property_list(backfill = backfill)
	total_count = len(properties)
	print "Total Properties: ", total_count
	count = 0
	for prop in properties:
		try:
			features = get_features(prop['Id'])
			inventory.append(features)
			count += 1
		except:
			print "Count: ", count
			print "error id: ", prop['Id']
			print sys.exc_info()
		if count % 100 == 0:
			print "Crawled Properties: ", count
	return inventory

if __name__ == '__main__':
	print time.ctime()
	inventory = get_inventory()
	print time.ctime()



