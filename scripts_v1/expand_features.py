import get_features
from datetime import datetime
from dateutil import parser
import re


def binary_feat(s, target, apart, name = ""):
	outcome = s.lower().find(target)
	if outcome != -1:
		if name == "":
			apart[target] = 1
			return apart, outcome
		else: apart[name] = 1
#		return apart, outcome
	else:
		if name == "":
			apart[target] = ''
			return apart, outcome
		else: apart[name] = ''
#		return apart, outcome

def numerical_feat(s, target, apart, name):
	outcome = s.lower().find(target)
	if outcome != -1:
		value_target = s[:outcome].strip()
		if value_target == "":
			apart[name] = 1
			return apart
		if value_target[-1].isdigit():
			apart[name] = int(value_target[-1])
		else: apart[name] = 1
		return apart
	else:
		apart[name] = ''
		return apart





def expand_features(apart):
	# get total number of rooms
	num_rooms_string = apart["number_rooms"]
	apart["number_rooms"] = ""
	apart["number_bedrooms"] = ""
	num_rooms_list = []
	for s in num_rooms_string.split():
		if s.isdigit():
			num_rooms_list.append(int(s))
	if len(num_rooms_list) == 2:
		apart["number_rooms"] = num_rooms_list[0]
		apart["number_of_bedrooms"] = num_rooms_list[1]
	if len(num_rooms_list) == 1:
		apart["number_of_rooms"] = num_rooms_list[0]


	# classify type of apartment
	ap_typ = apart["type_of_apartment"]
	if ap_typ.find("Upstairs apartment") != -1:
		apart["type_of_apartment"] = "Upstairs apartment"
	if ap_typ.lower().find("ground-floor") != -1:
		apart["type_of_apartment"] = "ground-floor"
	if ap_typ.lower().find("maisonnette") != -1:
		apart["type_of_apartment"] = "maisonnette"
	
	if ap_typ.lower().find("double") != -1:
		apart["double apt"] = 1
	else: apart["double apt"] = 0
	
	if ap_typ.lower().find("penthouse") != -1:
		apart["type_of_apartment"] = "penthouse"
	
	if ap_typ.lower().find("shared entrance") != -1:
		apart["shared entrance"] = 1
	else: apart["shared entrance"] = 0
	
	if ap_typ.lower().find("mezzanine") != -1:
		apart["type_of_apartment"] = "mezzanine"
	if ap_typ.lower().find("galleried") != -1:
		apart["type_of_apartment"] = "galleried"

	# periodic contribution

	per_cont = apart["periodic_contribution"]
	if per_cont.lower().find("no"):
		apart["periodic_contribution"] = [0]
	if per_cont.lower().find("yes"):
		periodic = [1]
		for s in per_cont.split():
			if s.isdigit():
				periodic.append(s)
		apart["periodic_contribution"] = periodic

	# facilities refinement

	facilities = apart["facilities"]
	if facilities.lower().find("mechanical ventilation") != -1:
		apart["mechanical_vent"] = 1
	else:
		apart["mechanical_vent"] = 0
	
	if facilities.lower().find("elevator") != -1:
		apart["elevator"] = 1
	else: apart["elevator"] = 0
	
	if facilities.lower().find("TV via cable") != -1:
		apart["TV"] = 1
	else: apart["TV"] = 0

	if facilities.lower().find("alarm") != -1:
		apart["alarm"] = 1
	else: apart["alarm"] = 0

	if facilities.lower().find("sauna") != -1:
		apart["sauna"] = 1
	else: apart["sauna"] = 0

	if facilities.lower().find("jacuzzi") != -1:
		apart["jacuzzi"] = 1
	else: apart["jacuzzi"] = 0

	if facilities.lower().find("swimming") != -1:
		apart["swimming pool"] = 1
	else: apart["swimming pool"] = 0

	if facilities.lower().find("electricity") != -1:
		apart["electricity"] = 1
	else: apart["electricity"] = 0


	# insulation refinement. From now on the binary_feat function is used.

	insulation = apart["insulation"]
	binary_feat(insulation, "completely", apart, "completely_insulated")
	binary_feat(insulation, "double glazing", apart)
	binary_feat(insulation, "floor insulation", apart)
	binary_feat(insulation, "floor insulation", apart)
	binary_feat(insulation, "secondary glazing", apart)
	binary_feat(insulation, "insulated walls", apart)

	#balcony
	balcony = apart["balcony"]
	binary_feat(balcony, "roof terrace", apart)
	binary_feat(balcony, "french balcony", apart)
	binary_feat(balcony, "balcony present", apart, "balcony")
	binary_feat(balcony, "roof terrace", apart)

	#number of bathrooms
	number_baths = apart["number_of_bathrooms"]
	apart["number_of_bathrooms"] = ''
	apart["number_of_toilets"] = ''
	num_baths_list = []
	for s in number_baths.split():
		if s.isdigit():
			num_baths_list.append(int(s))
	if len(num_baths_list) == 2:
		apart["number_of_bathrooms"] = num_baths_list[0]
		apart["number_of_toilets"] = num_baths_list[1]
	if len(num_baths_list) == 1:
		apart["number_of_bathrooms"] = num_baths_list[0]

	# bathroom facilities

	bathroom_facilities = apart["bathroom_facilities"]
	binary_feat(bathroom_facilities, 'jacuzzi', apart)
	binary_feat(bathroom_facilities, 'steam cabin', apart)
	numerical_feat(bathroom_facilities, 'shower', apart, "number of showers")
	numerical_feat(bathroom_facilities, 'bath', apart, 'number of baths')
	numerical_feat(bathroom_facilities, 'toilet', apart, 'number of toilets')
	binary_feat(bathroom_facilities, 'sauna', apart)

	#Boiler

	boiler = apart["CH_boiler"].lower()

	binary_feat(boiler, 'in ownership', apart, "boiler in ownership")
	binary_feat(boiler, 'gas fired', apart, 'gas fired boiler')

	#Building insurance

	insurance = apart['building_insurance'].lower()
	binary_feat(insurance, 'yes', apart, 'building insurance')

	#Listed since

	listed = apart['listed_since'].lower()
	w = listed.find("week")
	m = listed.find("month")

	if listed.find('6+ months') != -1:
		apart['days_since'] = 6*30
	elif w != -1:
		if listed[:w].strip()[-1].isdigit():
			apart['days_since'] = int(listed[:w].strip()[-1])*7
	elif m != -1:
		if listed[:m].strip()[-1].isdigit():
			apart['days_since'] = int(listed[:m].strip()[-1])*4*7
	else:
		try:
			dateobj = parser.parse(listed)
			snapshot_date = parser.parse(apart['snapshot_date'])
			days = snapshot_date - dateobj
			apart['days_since'] = days
		except:
			apart['days_since'] = ''

	#e_location

	location = apart['e_location'].lower()
	binary_feat(location, 'center', apart, 'central location')
	binary_feat(location, 'residential', apart, 'residential neighbourhood')
	binary_feat(location, 'water', apart, 'near water')
	binary_feat(location, 'busy road', apart, 'near busy road')
	binary_feat(location, 'unobstructed surrounding view', apart, 'unobstructed view')
	binary_feat(location, 'park', apart, 'near park')
	binary_feat(location, 'quiet road', apart, 'near quiet road')
	binary_feat(location, 'sheltered', apart, 'sheltered location')
	binary_feat(location, 'forest', apart, 'near forest')
	binary_feat(location, 'rural', apart, 'rural area')
	binary_feat(location, 'freestanding', apart, 'freestanding location')
	binary_feat(location, 'wooded', apart, 'wooded surroundings')

	#facilities

	facilities = apart['s_facilities'].lower()
	binary_feat(facilities, 'electricity', apart)
	binary_feat(facilities, 'heating_device', apart)
	binary_feat(facilities, 'running water', apart)

	#address

	location_string = apart['address']
	postcode = re.compile(r'\d\d\d\d\s\w\w')
	m = postcode.search(location_string)
	apart['postcode'] = m.group()
	apart['region identifier'] = m.group()[:2]
	apart['street identifier'] = (m.group()[2:4], m.group()[5:])

	street = re.compile(r'\D*')
	apart['street'] = street.match(location_string).group().rstrip()

	number = re.compile(r'\d+')
	n = number.search(location_string)
	apart['street number'] = n.group()

	apart['intern'] = location_string[n.end(): m.start()]


	#number of rooms

	num_rooms = apart['number_rooms']
	p = re.compile(r'\d')
	list_rooms = p.findall(num_rooms)
	if len(list_rooms) == 2:
		apart['number_of_rooms'] = int(list_rooms[0])
		apart['number_of_bedrooms'] = int(list_rooms[1])
	elif len(list_rooms) == 1:
		apart['number_of_rooms'] = int(list_rooms[0])
		apart['number_of_bedrooms']
	else:
		apart['number_of_rooms'] = ''
		apart['number_of_bedrooms'] = ''

	#CH boiler again
	boiler_again = apart['heating'].lower()
	binary_feat(boiler_again, 'ch boiler', apart, 'CH_boiler')
	binary_feat(boiler_again, 'floor insulation (partial)', apart, 'partial_floor_insulation')
	binary_feat(boiler_again, 'floor insulation (complete)', apart, 'complete_floor_insulation')
	binary_feat(boiler_again, 'communal', apart, 'communal_central_heating')
	binary_feat(boiler_again, 'fireplace', apart, 'fireplace')
	binary_feat(boiler_again, 'district heating', apart, 'district_heating')

	#specific info

	spec = apart['specific'].lower()
	binary_feat(spec, 'listed building', apart, 'listed_building')
	binary_feat(spec, 'monument', apart, 'monumental_building')
	binary_feat(spec, 'furnished', apart, 'furnished')
	binary_feat(spec, 'carpets', apart, 'furnished_carpets')
	binary_feat(spec, 'curtains', apart, 'furnished_curtains')
	binary_feat(spec, 'protected townscape', apart, 'protected_view')

	#Year of construction
	#we extract only the "end date" of the construction

	year = apart['year_of_construction'].lower()
	y = re.compile(r'\d\d\d\d')
	o = y.findall(year)
	if len(o) == 2:
		apart['final_year_of_construction'] = int(o[1])
	elif len(o) == 1:
		apart['final_year_of_construction'] = int(o[0])
	else:
		apart['final_year_of_construction'] = ''

	#located at
	located = apart['located_at'].lower()
	n = p.search(located)
	if located.find('ground floor') != -1:
		apart['level'] = 0
	elif n is not None:
		apart['level'] = int(n.group())
	else:
		apart['level'] = ''

	#number of stories
	stories = apart['number_of_layers'].lower()
	n = p.search(stories)
	if n is not None:
		apart['number_of_stories'] = int(n.group())
	else:
		apart['number_of_stories'] = ''














