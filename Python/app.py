from datetime import datetime, timedelta
import pickle
import urllib.request
import vt
import json
import os
import logging
import threading
from virus_total_classsification import virus_total_classification as vtc
import MySQLDB
from pandas import DataFrame
import pymysql
import time
with  open("./app.conf") as file_config:
    conf = json.load(file_config)

# configuration paramenters taken from app.conf

file_url = conf['file_url'] #'https://elementor-pub.s3.eu-central-1.amazonaws.com/Data-Enginner/Challenge1/request1.csv'
download_filepath=conf['download_filepath'] #'./test.csv'
minutes_to_add = conf['minutes_to_add'] #30
classifications_ttl_file= conf['classifications_ttl_file'] # './classifications_ttl.pickle'
classifications_file=conf['classifications_file'] #'./classifications.pickle'
API_KEY = conf['API_KEY'] #'[VIRUS_TOTAL_API_KEY]'

# dbObj=MySQLDB(conf['MYSQL'])

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
    try:
        url_id = vt.url_id(site)
        url = client.get_object("/urls/{}", url_id)
        logging.info("checking with VirusTotal api : {site}")
        return url.last_analysis_stats
    except:
        logging.error(f"unable to check with VirusTotal api : {site} ")
        return None
    client.close()

res = downloadFile(file_url,download_filepath)
if not res:
    raise Exception('Problem downloading file')

filereader = open(download_filepath)
classifications = {}
classifications_ttl = {}
classifications_ttl = load_from_pickle(filename = classifications_ttl_file)
classifications = load_from_pickle(filename = classifications_file)
list_classification_sites = []

for line in filereader:
    site=line.strip()
    if site in classifications and classifications_ttl[site] > datetime.now():
        continue
    else:
        # Connect to API
        # get json
        analysis_of_site = getFromVirusTotalAPI(site)
        if analysis_of_site is None:
            continue

        site_classification = vtc(site, analysis_of_site,minutes_to_add)
        classifications[site] = site_classification
        classifications_ttl[site] = site_classification.get_ttl()
        list_classification_sites.append(site_classification.to_row_in_array())
        time.sleep(5)

df = DataFrame (list_classification_sites, columns=['site', 'date', 'datetime', 'ttl', 'categoization', 'harmless', 'malicious', 'suspicious', 'timeout', 'undetected'])
if not df.empty:
    db = MySQLDB.MySQLDB(conf=conf['MYSQL'])
    db.add_to_db(df)
    db.close()

filereader.close()
save_to_pickle(classifications_ttl, classifications_ttl_file)
save_to_pickle(classifications, classifications_file)
