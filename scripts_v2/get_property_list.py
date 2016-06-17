#This program return a list of urls for property pages in a given geo
#backfill = True (default); otherwise only fetch the last three days data

#Need to do this for koop, huur and new
import requests
import json
import time

def get_property_list(geo = 'heel-nederland', backfill=False):
	property_list = []
	types = ['koop', 'huur', 'nieuwbouw']
	base_url = 'http://partnerapi.funda.nl/feeds/Aanbod.svc/search/\
json/c7e56d1972654b91bdd54fa12cf9d9c8/?website=funda&\
type=%s&\
zo=/%s/\
%s\
&page=%d\
&pagesize=25&projectObjectenTonen=2&objectTypenTonen=true&statistiekId=140'
	if backfill == False:
		days = '3-dagen'
	else:
		days = ''
	for tp in types:
		page = 1
		while True:
			url = base_url %(tp, geo, days, page)
			r = requests.get(url)
			data = r.json()
			property_list = property_list + data['Objects']
			page += 1
			total_pages = data['Paging']['AantalPaginas']
			if data['Paging']['VolgendeUrl'] == None:
				break
			if page % 100 == 0:
				print "getting type %s" %(tp), round(float(page) / total_pages, 3), time.ctime()
	return property_list


if __name__ == "__main__":
	l = get_property_list()
	with open('property_list.txt', 'w') as outfile:
		json.dump(l, outfile)
#	print l

