import urllib2
import requests
funda_base_url = 'http://www.funda.nl'


def get_next_target(s):
	start_link = s.find('<a href=')
	if start_link!= -1:
		#print "start link:", start_link
		start_quote = s.find('"', start_link)
		end_quote = s.find('"', start_quote + 1)
		#print "start and end:", start_quote," ",end_quote
		extension= s[start_quote :end_quote][1:]
		if extension.find('https://www.')!=-1 or extension.find('http://www.')!=-1:
			return extension, end_quote
		else:
			url = funda_base_url + extension
			return url, end_quote
	else:
		return [0,-1]



def get_all_links(input_url):
	try:
		response = urllib2.urlopen(input_url)
		page = response.read()
	except urllib2.HTTPError, error:
		page=error.read()
#	print page
#	try:
#		r = requests.get(input_url)
#		page = r.text
#	except 
	links = []
	while True:
		url, endpos = get_next_target(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links
