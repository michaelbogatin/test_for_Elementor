from datetime import datetime
import pickle
import urllib.request
import vt
import json
import os

with  open("./app.conf") as file_config:
    conf = json.load(file_config)

file_config.close()
# configuration paramenters taken from app.conf

file_url = conf['file_url'] #'https://elementor-pub.s3.eu-central-1.amazonaws.com/Data-Enginner/Challenge1/request1.csv'
download_filepath=conf['download_filepath'] #'./test.csv'
minutes_to_add = conf['minutes_to_add'] #30
classifications_ttl_file= conf['classifications_ttl_file'] # './classifications_ttl.pickle'
classifications_file=conf['classifications_file'] #'./classifications.pickle'
API_KEY = conf['API_KEY'] #'[VIRUS_TOTAL_API_KEY]'

def downloadFile(file_url = 'https://elementor-pub.s3.eu-central-1.amazonaws.com/Data-Enginner/Challenge1/request1.csv', download_filepath='./test.csv'):
    res=urllib.request.urlretrieve(file_url, download_filepath)
    return res

def load_from_pickle(filename):
    if not os.path.exists(filename):
        return {}
    infile = open(filename, 'rb')
    dic_from_pickle = pickle.load(infile)
    infile.close()
    return dic_from_pickle

def save_to_pickle(data,filepath):
    outfile = open(filepath, 'wb')
    pickle.dump(data, outfile)
    outfile.close()

def getFromVirusTotalAPI(site):
    client = vt.Client(API_KEY)
    analysis = client.scan_url(site)
    return analysis

res = downloadFile(file_url,download_filepath)
if not res:
    raise Exception('Problem downloading file')

filereader = open(download_filepath)
classifications = {}
classifications_ttl = {}
classifications_ttl = load_from_pickle(filename = classifications_ttl_file)
classifications = load_from_pickle(filename = classifications_file)

for line in filereader:
    site=line.strip()
    if site in classifications  and classifications_ttl[site] > datetime.now() :
        continue
        #classification[site]
    else :
        # Connect to API
        # get json
        analysis_of_site = getFromVirusTotalAPI(site)
        classifications[site] = analysis_of_site
        current_date_and_time = datetime.datetime.now()
        date_time_ttl = current_date_and_time + timedelta(minutes = minutes_to_add)
        classifications_ttl[site] = date_time_ttl

filereader.close()
save_to_pickle(classifications_ttl, classifications_ttl_file)
save_to_pickle(classifications, classifications_file)


