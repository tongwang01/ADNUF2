import csv
import get_features
import expand_features
import unicodecsv

sample_url = "http://www.funda.nl/koop/amsterdam/appartement-49453167-van-boetzelaerstraat-34-2/"


header_output = unicodecsv.writer(open("expanded_headers.csv", "wb"), encoding='utf-8', delimiter='|')
sample = get_features.get_features(sample_url)
sample["type"] = "sample"
expand_features.expand_features(sample)
header_output.writerow(sample.keys())