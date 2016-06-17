import get_all_links
import urllib2
import csv
import requests

root_url_huur = 'http://www.funda.nl/huur/amsterdam/'
root_url_verhuurd = 'http://www.funda.nl/huur/verhuurd/amsterdam/'
root_url_koop = 'http://www.funda.nl/koop/amsterdam/'
root_url_verkocht = 'http://www.funda.nl/koop/verkocht/amsterdam/'

#output_file = csv.writer(open("fundaAmsterdam_URLs_20150516.csv", "wb"))
#koop_file = csv.writer(open("fundaAmsterdamApart_koop_20150516.csv", "wb"))
#verkocht_file = csv.writer(open("fundaAmsterdamApart_verkocht_20150516.csv", "wb"))

#Define get aparts function, num_huur is the number of pages for huur, 
#num_pg_verhuurd is the number of pages for verhuurd
def get_aparts(num_pg_huur = 60, num_pg_verhuurd = 230, num_pg_koop = 390, num_pg_verkocht = 760):
	"""Get the list of urls for all apartment pages on Funda"""
	count = 0
	huur = []
	verhuurd = []
	huur_pg = []
	verhuurd_pg = []
	koop = []
	verkocht = []
	koop_pg = []
	verkocht_pg = []
	for i in range(1, num_pg_huur):
		new_page_url = root_url_huur + "p" + str(i) + "/"
		huur_pg.append(new_page_url)
	for i in range(1, num_pg_verhuurd):
		new_page_url = root_url_verhuurd + "p" + str(i) + "/"
		verhuurd_pg.append(new_page_url)
	for i in range(1, num_pg_koop):
		new_page_url = root_url_koop + "p" + str(i) + "/"
		koop_pg.append(new_page_url)
	for i in range(1, num_pg_verkocht):
		new_page_url = root_url_verkocht + "p" + str(i) + "/"
		verkocht_pg.append(new_page_url)

	print "Now crawling huur urls :)"
	for url in huur_pg:
		all_links = get_all_links.get_all_links(url)
		for link in all_links:
			if is_apart(link) and (link not in huur):
				huur.append(link)
#				output_file.writerow([link, "huur"])
				count += 1
				if count % 100 == 0:
					print "We have gathered urls: " + str(count)
	
	print "Now crawling verhuurd urls :)"
	for url in verhuurd_pg:
		all_links = get_all_links.get_all_links(url)
		for link in all_links:
			if is_apart(link) and (link not in verhuurd):
				verhuurd.append(link)
#				output_file.writerow([link, "verhuurd"])
				count += 1
				if count % 100 == 0:
					print "We have gathered urls: " + str(count)

	print "Now crawling koop urls :)"
	for url in koop_pg:
		all_links = get_all_links.get_all_links(url)
		for link in all_links:
			if is_apart(link) and (link not in koop):
				koop.append(link)
#				output_file.writerow([link, "koop"])
				count += 1
				if count % 100 == 0:
					print "We have gathered urls: " + str(count)

	print "Now crawling verkocht urls :)"
	for url in verkocht_pg:
		all_links = get_all_links.get_all_links(url)
		for link in all_links:
			if is_apart(link) and (link not in verkocht):
				verkocht.append(link)
#				output_file.writerow([link, "verkocht"])
				count += 1
				if count % 100 == 0:
					print "We have gathered urls: " + str(count)

	return (huur, verhuurd, koop, verkocht)

#def crawl_web(root_url):
#	print "crawl_web called"
#	aparts = []
#	to_crawl=[]
#	crawled = []
#	outgoing = []
#	to_crawl= get_all_links.get_all_links(root_url)
#	while len(to_crawl)>0:
#		new_link=to_crawl.pop()
#		if within_website(new_link):
#			print "new_link:" + new_link
#			child_links=get_all_links.get_all_links(new_link)
#			crawled.append(new_link)
#			to_add=[x for x in child_links if (x not in crawled and x not in to_crawl)]
#			to_crawl+=to_add
#			if is_apart(new_link) and (new_link not in aparts):
#				aparts_file.writerow([new_link])
#				aparts.append(new_link)
#				print "new_link:" + new_link
#		else:
#			if new_link not in outgoing:
#				outgoing.append(new_link)
#	return [crawled]

def within_website(url):
	"""Check whether a link point within Funda"""
	a = (url.find('www.funda.nl/koop/amsterdam/') != -1)
	return a

def is_apart(url):
	"""Check whether a url is an apartment page"""
	a = (url.find('www.funda.nl/huur/amsterdam/appartement-') != -1)
	b = (url.find('www.funda.nl/huur/verhuurd/amsterdam/appartement-') != -1)
	d = (url.find('www.funda.nl/koop/amsterdam/appartement-') != -1)
	e = (url.find('www.funda.nl/koop/verkocht/amsterdam/appartement-') != -1)
	c = (url.find('fotos/') == -1 and url.find('kenmerken/') == -1 
		and url.find('omschrijving/') == -1 and url.find('reageer/') == -1
		and url.find('doorsturen/') == -1 and url.find('print/') == -1
		and url.find('meld-een-fout/') == -1 and url.find('bezichtiging/') == -1
		and url.find('brochure/') == -1)
	return (a or b or d or e) and c

#Run get_aparts with 51 pages of huur and 203 pages of verhuurd
#a = get_aparts(51, 203)
