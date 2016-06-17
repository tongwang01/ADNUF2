#This program takes in an id for a property  and return a dict of properties
import requests

#sample_id = 'b9bc59b1-1661-4dbd-8ccb-ffd98f987adb'
sample_id = 'b780de47-8715-4726-b4e6-813802954711'

def get_features(id):
	base_url = 'http://partnerapi.funda.nl/feeds/Aanbod.svc/json/\
detail/c7e56d1972654b91bdd54fa12cf9d9c8/koop/\
%s/'
	url = base_url %(id)
	r = requests.get(url)
	return r.json()

if __name__ == '__main__':
	print get_features(sample_id)