import csv
import sys
import get_features
import unicodecsv
import get_url_list
import threading
import time

sample_url = "http://www.funda.nl/koop/amsterdam/appartement-49453167-van-boetzelaerstraat-34-2/"


def get_inventory(inventory, url_list):
#	failed_urls = 	unicodecsv.writer(open("failed_urls_all_threading_20150516.csv", "wb"), encoding='utf-8', delimiter='|')
	count = 0
	#Loop through all huur and verhuurd urls
	for row in url_list:
		try:
			apart = get_features.get_features(row[0])
			apart["type"] = row[1]
			inventory.append(apart)
		except:
			print "error url:" + row[0]
			print sys.exc_info()
#			failed_urls.writerow([row[0], sys.exc_info()])
		count += 1
		if count % 100 == 0:
			print "We have gathered properties: " + str(count)
		time.sleep(2)

def get_chunks(MyList, n):
	return [MyList[x:x+n] for x in range(0, len(MyList), n)]

def main():
	inventory = []
	huur, verhuurd, koop, verkocht = get_url_list.get_aparts(60, 230, 390, 760)
	url_list = []
	#Compile the four lists into one
	for item in huur:
		url_list.append([item, "huur"])
	for item in verhuurd:
		url_list.append([item, "verhurrd"])
	for item in koop:
		url_list.append([item, "koop"])
	for item in verkocht:
		url_list.append([item, "verkocht"])
	print "Done getting all the urls!"	

	new_url_list = get_chunks(url_list, 1000)
	threads = []
	for i in range(len(new_url_list)):
		t = threading.Thread(target = get_inventory, args=(inventory, new_url_list[i], ))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()
		
	print "Done getting all the features!"

	threading_output = unicodecsv.writer(open("FundaInventoryLatest.csv", "wb"), encoding='utf-8', delimiter='|')
	sample = get_features.get_features(sample_url)
	sample["type"] = "sample"
	threading_output.writerow(sample.keys())
	for row in inventory:
		threading_output.writerow(row.values())
	print "Done writing output file!"

if __name__ == "__main__":
    main()





